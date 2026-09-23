const PYODIDE_INDEX = "https://cdn.jsdelivr.net/pyodide/v0.29.5/full/";
const WHEEL_FILE = "barebones_tts-0.1.0-py3-none-any.whl";

const ta = document.getElementById("text");
const btnSpeak = document.getElementById("speak");
const btnSave = document.getElementById("save");
const btnClear = document.getElementById("clear");
const consoleEl = document.getElementById("console");

let pyodide = null;
let glueSpeak = null;
let glueSave = null;
let ready = false;
let busy = false;

const T0 = performance.now();
let stageStart = T0;
let currentStage = "start";

function report(event, fields = {}) {
  try {
    if (!navigator.sendBeacon) return;
    const now = performance.now();
    const data = JSON.stringify({
      event,
      ms: Math.round(now - stageStart),
      total_ms: Math.round(now - T0),
      ...fields,
    });
    stageStart = now;
    navigator.sendBeacon("/_log", data);
  } catch {
  }
}

function addLine(text, className) {
  const div = document.createElement("div");
  div.className = className || "";
  div.textContent = text;
  consoleEl.appendChild(div);
  consoleEl.scrollTop = consoleEl.scrollHeight;
}

function sys(text) { addLine(text, "sys"); }
function err(text) { addLine(text, "err"); }

const ANSI = {
  30: "c30", 31: "c31", 32: "c32", 33: "c33",
  34: "c34", 35: "c35", 36: "c36", 37: "c37",
  90: "c90", 91: "c91", 92: "c92", 93: "c93",
  94: "c94", 95: "c95", 96: "c96", 97: "c97",
};

function ansiToFragment(text) {
  const frag = document.createDocumentFragment();
  let cls = null;
  let buf = "";
  const flush = () => {
    if (!buf) return;
    const span = document.createElement("span");
    if (cls) span.className = cls;
    span.textContent = buf;
    frag.appendChild(span);
    buf = "";
  };
  const re = /\x1b\[([0-9;]*)m/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    buf += text.slice(last, m.index);
    last = re.lastIndex;
    flush();
    cls = null;
    for (const code of m[1].split(";")) {
      if (code === "" || code === "0" || code === "39") { cls = null; continue; }
      if (ANSI[code]) cls = ANSI[code];
    }
  }
  buf += text.slice(last);
  flush();
  return frag;
}

function out(text) {
  for (const line of String(text).split("\n")) {
    if (line === "") continue;
    const div = document.createElement("div");
    div.appendChild(ansiToFragment(line));
    consoleEl.appendChild(div);
  }
  consoleEl.scrollTop = consoleEl.scrollHeight;
}

let audioCtx = null;

async function playWav(bytes) {
  try {
    audioCtx = audioCtx || new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === "suspended") {
      await Promise.race([audioCtx.resume(), new Promise((r) => setTimeout(r, 1500))]);
    }

    const copy = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
    const buf = await audioCtx.decodeAudioData(copy);

    const src = audioCtx.createBufferSource();
    src.buffer = buf;
    src.connect(audioCtx.destination);
    src.start();
    addLine(`playing ${buf.duration.toFixed(2)}s of audio`);
  } catch (e) {
    addLine(`playback unavailable in this environment (${e.message ?? e})`);
    report("playback_error", { message: String(e.message ?? e).slice(0, 300) });
  }
}


function fmtBytes(n) {
  return n < 1024 ? `${n} B` : `${(n / 1024).toFixed(1)} KiB`;
}

function ensureBytes(v) {
  if (v instanceof Uint8Array) return v;
  if (v && typeof v.toJs === "function") {
    const b = v.toJs();
    if (v.destroy) v.destroy();
    return b;
  }
  throw new Error(`unexpected return type from python: ${typeof v}`);
}

const paint = () => new Promise((r) => requestAnimationFrame(() => setTimeout(r, 0)));

function refreshButtons() {
  btnSpeak.disabled = !ready || busy || ta.value.trim() === "";
  btnSave.disabled = !ready || busy || ta.value.trim() === "";
}

function setBusy(state) {
  busy = state;
  refreshButtons();
}

async function withText(action) {
  if (!ready || busy) return;
  const text = ta.value.trim();
  if (!text) {
    err("text box is empty");
    return;
  }
  setBusy(true);
  addLine(`> ${text}`);
  await paint();
  try {
    await action(text);
  } catch (e) {
    err(e && e.message ? e.message : String(e));
    report("error", { message: String(e?.message ?? e).slice(0, 300), source: "action" });
  } finally {
    setBusy(false);
  }
}

const onSpeak = () => withText(async (text) => {
  const wav = ensureBytes(glueSpeak(text));
  await playWav(wav);
  report("speak"); //this is just the timing data. your inputs arent recorded
});

const onSave = () => withText(async (text) => {
  const res = glueSave(text);
  const [filename, data] = res.toJs();
  res.destroy();

  const blob = new Blob([data], { type: "audio/wav" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 10_000);

  addLine(`saved ${filename} (${fmtBytes(data.length)})`);
  await playWav(ensureBytes(data));
  report("save", { bytes: data.length });
});


async function boot() {
  sys("loading python runtime (pyodide)...");
  currentStage = "pyodide";
  pyodide = await loadPyodide({ indexURL: PYODIDE_INDEX });
  pyodide.setStdout({ batched: (s) => out(s) });
  pyodide.setStderr({ batched: (s) => err(s) });
  report("boot", { stage: "pyodide" });

  sys("loading numpy and scipy...");
  currentStage = "packages";
  await pyodide.loadPackage(["numpy", "scipy", "micropip"]);
  await pyodide.runPythonAsync(
    'import numpy, scipy; print(f"numpy {numpy.__version__}, scipy {scipy.__version__}")'
  );
  report("boot", { stage: "packages" });

  sys("installing barebones-tts...");
  currentStage = "wheel";
  const micropip = pyodide.pyimport("micropip");
  await micropip.install(new URL(WHEEL_FILE, location.href).href);
  const glueSrc = await (await fetch("glue.py")).text();
  await pyodide.runPythonAsync(glueSrc);
  report("boot", { stage: "wheel" });

  glueSpeak = pyodide.globals.get("speak_wav");
  glueSave = pyodide.globals.get("save_wav_file");

  ready = true;
  refreshButtons();
  currentStage = "ready";
  report("boot", { stage: "ready" });
}

boot().catch((e) => {
  err(`failed to start: ${e.message ?? e}`);
  report("boot_error", { stage: currentStage, message: String(e.message ?? e).slice(0, 300) });
});

addEventListener("error", (e) => {
  report("error", {
    message: String(e.message ?? "unknown error").slice(0, 300),
    source: e.filename ? e.filename.split("/").pop() : "",
    line: e.lineno ?? 0,
  });
});

addEventListener("unhandledrejection", (e) => {
  const reason = e.reason?.message ?? String(e.reason ?? "unhandled rejection");
  report("error", { message: reason.slice(0, 300), source: "promise" });
});


btnSpeak.addEventListener("click", onSpeak);
btnSave.addEventListener("click", onSave);

ta.addEventListener("input", refreshButtons);

ta.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") { e.preventDefault(); onSpeak(); }
});

btnClear.addEventListener("click", () => {
  consoleEl.textContent = "";
});

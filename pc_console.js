(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.PcConsoleCommands = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  const LIMITS = {
    x: { min: -9999999, max: 99999999 },
    y: { min: -9999999, max: 99999999 },
    p: { min: -9999999, max: 99999999 },
    jog: { min: 1, max: 100000 },
  };

  function clampNumber(value, min, max) {
    const number = Number.parseInt(String(value), 10);
    if (Number.isNaN(number)) return 0;
    return Math.max(min, Math.min(max, number));
  }

  function fixedField(value, width) {
    const number = clampNumber(value, -9999999, 99999999);
    const sign = number < 0 ? "-" : "";
    const digits = Math.abs(number).toString().padStart(width - sign.length, "0");
    return (sign + digits).slice(0, width);
  }

  function moveAbsCommand(x, y, p) {
    return `CMOVEABS;${fixedField(x, 8)};${fixedField(y, 8)};${fixedField(p, 8)}`;
  }

  function powerCommand(enabled) {
    return enabled ? "CPOWERON" : "CPOWEROF";
  }

  function jogTarget(axis, direction, step, state) {
    const key = String(axis).toLowerCase();
    if (!["x", "y", "p"].includes(key)) {
      throw new Error("Unknown axis");
    }

    const safeStep = clampNumber(step, LIMITS.jog.min, LIMITS.jog.max);
    const current = clampNumber(state[key] || 0, LIMITS[key].min, LIMITS[key].max);
    return {
      ...state,
      [key]: clampNumber(current + (direction < 0 ? -safeStep : safeStep), LIMITS[key].min, LIMITS[key].max),
    };
  }

  function buildPowerShell(host, port, command) {
    const safeHost = String(host || "10.101.10.150").replace(/"/g, "");
    const safePort = clampNumber(port || 1985, 1, 65535);
    const safeCommand = String(command || "").replace(/"/g, "");
    return [
      `$client = [System.Net.Sockets.TcpClient]::new("${safeHost}",${safePort})`,
      "$stream = $client.GetStream()",
      `$msg = [Text.Encoding]::ASCII.GetBytes("${safeCommand}")`,
      "$stream.Write($msg,0,$msg.Length)",
      "$client.Close()",
    ].join("\n");
  }

  return {
    LIMITS,
    clampNumber,
    fixedField,
    moveAbsCommand,
    powerCommand,
    jogTarget,
    buildPowerShell,
  };
});

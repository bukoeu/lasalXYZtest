const assert = require("assert");
const fs = require("fs");
const path = require("path");
const commands = require("../pc_console.js");

const root = path.resolve(__dirname, "..");

assert.strictEqual(commands.fixedField(0, 8), "00000000");
assert.strictEqual(commands.fixedField(1000, 8), "00001000");
assert.strictEqual(commands.fixedField(-25, 8), "-0000025");
assert.strictEqual(commands.moveAbsCommand(1000, 2000, 0), "CMOVEABS;00001000;00002000;00000000");
assert.strictEqual(commands.powerCommand(true), "CPOWERON");
assert.strictEqual(commands.powerCommand(false), "CPOWEROF");

const jogged = commands.jogTarget("x", 1, 100, { x: 10, y: 20, p: 30 });
assert.deepStrictEqual(jogged, { x: 110, y: 20, p: 30 });

const ps = commands.buildPowerShell("10.101.10.150", 1985, "CPOWERON");
assert.ok(ps.includes("TcpClient"));
assert.ok(ps.includes("CPOWERON"));

const html = fs.readFileSync(path.join(root, "pc_console.html"), "utf8");
assert.ok(html.includes("PC Steuerkonsole"));
assert.ok(html.includes("pc_console.js"));
assert.ok(html.includes("CMOVEABS"));

console.log("pc_console tests passed");

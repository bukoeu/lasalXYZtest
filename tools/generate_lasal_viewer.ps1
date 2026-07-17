param(
    [string]$ProjectRoot = "C:\tmp\LSLCL2\LASAL",
    [string]$OutputFile = "C:\Users\Admin\Documents\LSLCL2\lasal_viewer.html"
)

$ErrorActionPreference = "Stop"

function HtmlEscape([string]$Text) {
    if ($null -eq $Text) { return "" }
    return [System.Net.WebUtility]::HtmlEncode($Text)
}

function JsString([string]$Text) {
    if ($null -eq $Text) { return '""' }
    return '"' + (($Text -replace '\\', '\\') -replace '"', '\"' -replace "`r", '' -replace "`n", '\n') + '"'
}

function RelPath([string]$Path) {
    return $Path.Substring($ProjectRoot.Length).TrimStart('\')
}

if (-not (Test-Path -LiteralPath $ProjectRoot)) {
    throw "ProjectRoot not found: $ProjectRoot"
}

$extensions = @(".st", ".h", ".cpp", ".lcp", ".lcn", ".lda", ".md", ".xml", ".txt")
$files = Get-ChildItem -LiteralPath $ProjectRoot -Recurse -File -Force |
    Where-Object { $extensions -contains $_.Extension.ToLowerInvariant() } |
    Sort-Object FullName

$items = foreach ($file in $files) {
    $rel = RelPath $file.FullName
    $category = if ($rel -like "Class\*") { "Class" }
        elseif ($rel -like "Network\*") { "Network" }
        elseif ($rel -like "Drive\*") { "Drive" }
        elseif ($rel -like "Include\*") { "Include" }
        elseif ($rel -like "Source\*") { "Source" }
        else { "Root" }

    $text = ""
    try {
        $text = Get-Content -LiteralPath $file.FullName -Raw -ErrorAction Stop
    } catch {
        $text = ""
    }

    $lines = @()
    if ($text) {
        $allLines = $text -split "`r?`n"
        for ($i = 0; $i -lt $allLines.Count; $i++) {
            $line = $allLines[$i]
            if ($line -match '\b(CLASS|FUNCTION|METHOD|STATE|TCP|Command|Axis|Move|Safety|VARAN|SDIAS|PickPlace|XAxis|YAxis|ZAxis)\b') {
                $lines += @{
                    n = $i + 1
                    t = $line.Trim()
                }
            }
            if ($lines.Count -ge 25) { break }
        }
    }

    [PSCustomObject]@{
        rel = $rel
        name = $file.Name
        category = $category
        ext = $file.Extension
        kb = [math]::Round($file.Length / 1KB, 1)
        url = ("file:///" + ($file.FullName -replace '\\', '/'))
        hits = $lines
    }
}

$counts = $items | Group-Object category | Sort-Object Name
$jsonRows = foreach ($item in $items) {
    $hitJson = (($item.hits | ForEach-Object {
        "{n:$($_.n),t:$(JsString $_.t)}"
    }) -join ",")
    "{rel:$(JsString $item.rel),name:$(JsString $item.name),category:$(JsString $item.category),ext:$(JsString $item.ext),kb:$($item.kb),url:$(JsString $item.url),hits:[$hitJson]}"
}
$dataJson = "[" + ($jsonRows -join ",`n") + "]"

$summaryRows = foreach ($group in $counts) {
    "<span class='pill'>$($group.Name): $($group.Count)</span>"
}

$html = @"
<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LASAL Offline Viewer</title>
  <style>
    :root { color-scheme: light; --bg:#f7f8fa; --panel:#ffffff; --ink:#17202a; --muted:#607080; --line:#d8dee6; --accent:#1f6feb; --soft:#eef4ff; }
    * { box-sizing: border-box; }
    body { margin:0; font-family: Segoe UI, Arial, sans-serif; color:var(--ink); background:var(--bg); }
    header { position: sticky; top:0; z-index:2; background:var(--panel); border-bottom:1px solid var(--line); padding:14px 18px; }
    h1 { margin:0 0 8px; font-size:22px; font-weight:650; }
    .meta { display:flex; flex-wrap:wrap; gap:8px; color:var(--muted); font-size:13px; }
    .pill { border:1px solid var(--line); background:#fff; border-radius:999px; padding:4px 9px; }
    .layout { display:grid; grid-template-columns: 300px 1fr; min-height: calc(100vh - 89px); }
    aside { border-right:1px solid var(--line); background:#fff; padding:14px; position:sticky; top:89px; height:calc(100vh - 89px); overflow:auto; }
    main { padding:18px; }
    input, select { width:100%; padding:10px 11px; border:1px solid var(--line); border-radius:6px; font-size:14px; background:#fff; }
    label { display:block; font-size:12px; color:var(--muted); margin:12px 0 5px; }
    .tabs { display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:12px; }
    button { border:1px solid var(--line); background:#fff; border-radius:6px; padding:9px; cursor:pointer; }
    button.active { border-color:var(--accent); background:var(--soft); color:var(--accent); }
    .card { background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:14px; margin-bottom:12px; }
    .row { display:flex; align-items:flex-start; justify-content:space-between; gap:14px; }
    .path { font-family: Consolas, monospace; font-size:13px; overflow-wrap:anywhere; }
    .small { color:var(--muted); font-size:12px; }
    a { color:var(--accent); text-decoration:none; }
    a:hover { text-decoration:underline; }
    pre { white-space:pre-wrap; margin:8px 0 0; background:#f2f4f7; border:1px solid var(--line); padding:10px; border-radius:6px; font-family:Consolas, monospace; font-size:12px; line-height:1.45; }
    .hit { display:grid; grid-template-columns:54px 1fr; gap:8px; }
    .line { color:var(--muted); text-align:right; }
    .empty { color:var(--muted); padding:22px; text-align:center; }
    .quick { display:grid; gap:8px; }
    .quick a { display:block; padding:7px 8px; border-radius:6px; color:var(--ink); }
    .quick a:hover { background:var(--soft); text-decoration:none; }
    @media (max-width: 820px) {
      .layout { grid-template-columns:1fr; }
      aside { position:static; height:auto; border-right:0; border-bottom:1px solid var(--line); }
    }
  </style>
</head>
<body>
  <header>
    <h1>LASAL Offline Viewer</h1>
    <div class="meta">
      <span class="pill">Projekt: $(HtmlEscape $ProjectRoot)</span>
      <span class="pill">Dateien: $($items.Count)</span>
      $($summaryRows -join "`n      ")
    </div>
  </header>
  <div class="layout">
    <aside>
      <label for="q">Suche</label>
      <input id="q" placeholder="z.B. TCP, PickPlace, ZAxis, FUNCTION">
      <label for="cat">Bereich</label>
      <select id="cat">
        <option value="">Alle Bereiche</option>
        <option>Class</option>
        <option>Network</option>
        <option>Drive</option>
        <option>Include</option>
        <option>Source</option>
        <option>Root</option>
      </select>
      <div class="tabs">
        <button id="allBtn" class="active">Alle</button>
        <button id="hitsBtn">Nur Treffer</button>
      </div>
      <label>Schnellzugriff</label>
      <div class="quick">
        <a href="file:///C:/tmp/LSLCL2/LASAL/LASAL.lcp">LASAL.lcp</a>
        <a href="file:///C:/tmp/LSLCL2/LASAL/Class/Controller/Controller.st">Controller.st</a>
        <a href="file:///C:/tmp/LSLCL2/LASAL/Class/NCController/NCController.st">NCController.st</a>
        <a href="file:///C:/tmp/LSLCL2/LASAL/Class/MoveController/MoveController.st">MoveController.st</a>
        <a href="file:///C:/tmp/LSLCL2/LASAL/Network/PickPlace/PickPlace.lcn">PickPlace.lcn</a>
        <a href="file:///C:/tmp/LSLCL2/LASAL/Network/XAxis/XAxis.lcn">XAxis.lcn</a>
      </div>
    </aside>
    <main>
      <div id="result"></div>
    </main>
  </div>
  <script>
    const files = $dataJson;
    const q = document.getElementById('q');
    const cat = document.getElementById('cat');
    const result = document.getElementById('result');
    const allBtn = document.getElementById('allBtn');
    const hitsBtn = document.getElementById('hitsBtn');
    let onlyHits = false;

    function esc(s) {
      return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    }

    function matches(item, term) {
      const hay = [item.rel, item.name, item.category, item.ext, ...item.hits.map(h => h.t)].join(' ').toLowerCase();
      return hay.includes(term);
    }

    function render() {
      const term = q.value.trim().toLowerCase();
      const category = cat.value;
      let rows = files.filter(f => (!category || f.category === category) && (!term || matches(f, term)));
      if (onlyHits) rows = rows.filter(f => f.hits.length);
      rows = rows.slice(0, 250);

      if (!rows.length) {
        result.innerHTML = '<div class="empty">Keine Dateien gefunden.</div>';
        return;
      }

      result.innerHTML = rows.map(f => {
        const hits = f.hits.length
          ? '<pre>' + f.hits.map(h => '<span class="hit"><span class="line">' + h.n + '</span><span>' + esc(h.t) + '</span></span>').join('') + '</pre>'
          : '<div class="small">Keine extrahierten Schluesselzeilen.</div>';
        return '<section class="card">'
          + '<div class="row"><div><div class="path">' + esc(f.rel) + '</div><div class="small">' + esc(f.category) + ' · ' + esc(f.ext || '(ohne Endung)') + ' · ' + f.kb + ' KB</div></div>'
          + '<a href="' + esc(f.url) + '">Oeffnen</a></div>'
          + hits
          + '</section>';
      }).join('');
    }

    q.addEventListener('input', render);
    cat.addEventListener('change', render);
    allBtn.addEventListener('click', () => { onlyHits = false; allBtn.classList.add('active'); hitsBtn.classList.remove('active'); render(); });
    hitsBtn.addEventListener('click', () => { onlyHits = true; hitsBtn.classList.add('active'); allBtn.classList.remove('active'); render(); });
    render();
  </script>
</body>
</html>
"@

Set-Content -LiteralPath $OutputFile -Value $html -Encoding UTF8
Write-Host "Viewer written to $OutputFile"

# 抓取 JavaGuide RAG 系列 6 个页面的原始 HTML（脚本放英文路径，内部用 $PSScriptRoot 定位）
$ErrorActionPreference = 'Continue'
$base = Split-Path $PSScriptRoot -Parent   # d:/Buaa_2026/AI-Learning-Route
$rawDir = Join-Path $base '讲义/第2周/RAG知识/_raw'
New-Item -ItemType Directory -Force -Path $rawDir | Out-Null

$urls = @(
  'https://javaguide.cn/ai/rag/rag-basis.html',
  'https://javaguide.cn/ai/rag/rag-document-processing.html',
  'https://javaguide.cn/ai/rag/rag-vector-store.html',
  'https://javaguide.cn/ai/rag/rag-knowledge-update.html',
  'https://javaguide.cn/ai/rag/graphrag.html',
  'https://javaguide.cn/ai/rag/rag-optimization.html'
)

$i = 1
foreach ($u in $urls) {
  $f = Join-Path $rawDir ("{0}.html" -f $i)
  try {
    Invoke-WebRequest -Uri $u -OutFile $f -UseBasicParsing -TimeoutSec 90
    $size = (Get-Item $f).Length
    Write-Host ("OK {0} size={1}" -f $i, $size)
  } catch {
    Write-Host ("FAIL {0} {1}" -f $i, $_.Exception.Message)
  }
  $i++
}

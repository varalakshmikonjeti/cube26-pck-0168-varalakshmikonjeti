$projectRoot = Resolve-Path "$PSScriptRoot\..\..\.."

Set-Location $projectRoot

$inputFile = Join-Path $PSScriptRoot "verification_request.json"

Get-Content $inputFile -Raw |
    python -m submissions.varalakshmikonjeti.src
# see http://blogs.msdn.com/b/webdev/archive/2012/08/22/visual-studio-project-compatability-and-visualstudioversion.aspx
$toolsets  = @("v120","v110","v100")
$platforms = @("Win32","x64")
$configs = @("Debug","Release")

$sln = "..\..\gflags-vs2013.sln"

foreach($platform in $platforms)
{
    foreach($config in $configs)
    {
        foreach($toolset in $toolsets)
        {
            Write-Host "#############################################################################"  -ForegroundColor Red
            Write-Host "Building $platform, $config, $toolset"  -ForegroundColor Red
            Write-Host "#############################################################################"  -ForegroundColor Red
            msbuild $sln /p:VisualStudioVersion=12.0 /p:PlatformToolset=$toolset /p:Platform=$platform /p:Configuration=$config
        }
    }
}

Write-NuGetPackage .\gflags.autopkg




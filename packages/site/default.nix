{
  lib,
  runCommand,
  pkgs,
}:

let
  gems = pkgs.bundlerEnv {
    name = "gems";
    gemdir = ../../.;
  };
in
runCommand "site"
  {
    nativeBuildInputs = [
      pkgs.gnumake
      gems
      (lib.lowPrio gems.wrappedRuby)
      pkgs.glibcLocales
    ];

    env = {
      THIRDPARTY_PHOTOSWIPE = pkgs.fetchzip {
        url = "https://github.com/dimsemenov/PhotoSwipe/archive/refs/tags/v4.1.2.zip";
        hash = "sha256-ibvQ6G+3LLwWCb9KboADakOHwkG3uXX54jDMh7LxHg4=";
      };
      LC_ALL = "en_US.UTF-8";
    };
  }
  ''
    cd ${../../.}
    make build
  ''

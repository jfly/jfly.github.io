{ lib, inputs, ... }:
{
  imports = [ inputs.devshell.flakeModule ];

  perSystem =
    { self', pkgs, ... }:
    let
      buildEnv =
        pkg:
        (pkg.overrideAttrs (oldAttrs: {
          passthru.buildEnv = oldAttrs.env;
        })).passthru.buildEnv;
    in
    {
      devshells.default = {
        packages = [
          pkgs.gnumake
          pkgs.bundix
        ];

        packagesFrom = [ self'.packages.site ];
        env = lib.attrsToList (buildEnv self'.packages.site);
      };
    };
}

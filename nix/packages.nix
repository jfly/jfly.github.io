{
  perSystem =
    { pkgs, ... }:
    {
      packages = {
        resize-images = pkgs.callPackage ../packages/resize-images { };
        site = pkgs.callPackage ../packages/site { };
      };
    };
}

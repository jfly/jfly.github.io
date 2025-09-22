{ inputs, ... }:
{
  imports = [
    inputs.treefmt-nix.flakeModule
    inputs.git-hooks-nix.flakeModule
  ];

  perSystem.pre-commit.settings.hooks.treefmt.enable = true;

  perSystem.treefmt.programs = {
    # Nix
    nixfmt.enable = true;
    # Python
    ruff-check.enable = true;
    ruff-format.enable = true;
    # Ruby
    rufo.enable = true;
  };
}

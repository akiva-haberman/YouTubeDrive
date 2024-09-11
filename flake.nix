{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python312;
      in
      {
        formatter = pkgs.nixpkgs-fmt;
        devShells.default = with pkgs; mkShell {
          packages = [ 
            cowsay
            ( python.withPackages (p: with p; [
            numpy
            pillow
            opencv4
          ])) ];
        };
      }
    );
}
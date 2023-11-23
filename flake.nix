{
  description = "Python Template";

  inputs = {
    nixpkgs.url = github:NixOS/nixpkgs/nixos-unstable;
    systems.url = "github:nix-systems/x86_64-linux";
    flake-utils = {
      url = github:numtide/flake-utils;
      inputs.systems.follows = "systems";
    };
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        env = { };
        pythonEnv = pkgs.python3.withPackages (ps: [
          ps.selenium
        ]);
        nativeBuildInputs = with pkgs; [
          makeWrapper
        ];
        buildInputs = with pkgs; [
          pythonEnv
          chromedriver
        ];
      in
      {
        devShells.default = pkgs.mkShell {
          inherit buildInputs nativeBuildInputs;
        };
        packages.default = pkgs.stdenv.mkDerivation {
          inherit buildInputs nativeBuildInputs;
          name = "liauto";
          src = ./.;
          installPhase = ''
            mkdir -p $out/bin
            cp -r ./main.py $out/bin/$name
            wrapProgram $out/bin/$name --prefix PATH : ${pkgs.chromedriver}/bin
          '';
        };
      }
    );
}

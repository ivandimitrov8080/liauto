{
  description = "Python Template";

  inputs = {
    nixpkgs.url = "nixpkgs";
    systems.url = "github:nix-systems/x86_64-linux";
    flake-utils = {
      url = "github:numtide/flake-utils";
      inputs.systems.follows = "systems";
    };
    ide = {
      url = "github:ivandimitrov8080/flake-ide";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, ide, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        env = { };
        nvim = ide.nvim.${system}.standalone {
          plugins = {
            lsp.servers = {
              pylsp.enable = true;
            };
          };
        };
        pythonEnv = pkgs.python3.withPackages (ps: [
          ps.selenium
        ]);
        nativeBuildInputs = with pkgs; [
          makeWrapper
        ];
        buildInputs = with pkgs; [
          pythonEnv
          chromedriver
          ungoogled-chromium
        ];
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            nvim
          ] ++ buildInputs;
        };
        packages.default = pkgs.stdenv.mkDerivation {
          inherit buildInputs nativeBuildInputs;
          name = "liauto";
          src = ./.;
          installPhase = ''
            mkdir -p $out/bin
            cp -r ./main.py $out/bin/$name
            wrapProgram $out/bin/$name --prefix PATH : ${pkgs.chromedriver}/bin:${pkgs.ungoogled-chromium}/bin
          '';
        };
      }
    );
}

{ pkgs, ... }: {
  # https://devenv.sh/packages/
  packages = [
    (import ./pulumi.nix { inherit pkgs; })
    pkgs.awscli2
    pkgs.go-task
  ];

  dotenv = {
    enable = false;
    filename = ".env";
  };

  # https://devenv.sh/languages/
  languages.python = {
    enable = true;
    poetry = {
      enable = true;
      install = {
        enable = true;
        groups = [ "main" "dev" ];
        allExtras = true;
      };
    };
    libraries = with pkgs; [zlib];
    version = "3.11";
  };
}

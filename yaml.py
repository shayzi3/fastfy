import argparse

from typing import Literal



def set_amvera_yaml(argument: Literal["bot", "backend"]) -> None:
     text = f"""
     meta:
     environment: python
     toolchain:
          name: pip
          version: 3.10.8
build:
     requirementsPath: {argument}/requirements.txt
     useCache: true
run:
     scriptName: {argument}/main.py
     command: null
     persistenceMount: /data
     containerPort: "8085"
     servicePort: "80"
     """
     with open("amvera.yaml", "w") as file:
          file.write(text.strip())
          
     print(f"yaml mode {argument}")
     
     
     
def main() -> None:
     parser = argparse.ArgumentParser()
     parser.add_argument("arg", type=str)
     args = parser.parse_args()
     set_amvera_yaml(argument=args.arg)
     

if __name__ == "__main__":
     main()
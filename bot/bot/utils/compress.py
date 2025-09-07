from typing import Literal



class CompressName:
     patterns_to = {
          "(Factory New)": "FN",
          "(Minimal Wear)": "MW",
          "(Field-Tested)": "FT",
          "(Well-Worn)": "WW",
          "(Battle-Scarred)": "BS",
          "StatTrak™": "ST",
          "Souvenir": "SV"
     }
     patterns_from = {
          "FN": "(Factory New)",
          "MW": "(Minimal Wear)",
          "FT": "(Field-Tested)",
          "WW": "(Well-Worn)",
          "BS": "(Battle-Scarred)",
          "ST": "StatTrak™",
          "SV": "Souvenir"
     }
     
     @classmethod
     def compress(
          cls, 
          skin_name: str, 
          mode: Literal["to", "from"]
     ) -> str:
          pattern = cls.patterns_to if mode == "to" else cls.patterns_from
          for ptr, prt_value in pattern.items():
               skin_name = skin_name.replace(ptr, prt_value)
          return skin_name
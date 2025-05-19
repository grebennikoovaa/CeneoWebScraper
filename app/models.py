import json
import os
import pandas as pd
import numpy as np

class Product:
    def __init__(self, product_id, product_name, opinions, stars):
        self.product_id = product_id
        self.product_name = product_name
        self.opinions = opinions
        self.stars = stars

    def __str__(self):
        return f"Product_id: {self.product_id}\nProduct_name: {self.product_name}\nOpinions: "+"\n\n".join(str(opinions)for opinions in self.opinions)

    def export_opinions(self):
       if not os.path.exists("./app/data"):
                os.mkdir("./app/data")
       if not os.path.exists("./app/data/opinions"):
           os.mkdir("./app/data/opinions")
       with open(f"./app/data/opinions/{self.product_id}.json","w", encoding="UTF-8") as jf:
          json.dump([opinion.transfor_to_dict() for opinion in self.opinions], jf, ensure_ascii=False, indent=4)

    
    def export_info(self):
       if not os.path.exists("./app/data"):
                os.mkdir("./app/data")
       if not os.path.exists("./app/data/opinions"):
           os.mkdir("./app/data/opinions")
       with open(f"./app/data/opinions/{self.product_id}.json","w", encoding="UTF-8") as jf:
          json.dump([opinion.transfor_to_dict() for opinion in self.opinions], jf, ensure_ascii=False, indent=4)

    def transform_to_dict(self):
         return {
                  "product_id": self.product_id,
                  "product_name": self.product_name,
                  "stats": self.stats
         }


    def import_opinions(self):
        with open(f"./app/data/opinions/{self.opinions_id}.json, "r", encoding="UTF-8"") as jf:
          opinions = json.load(jf)
          for opinion in opinions:
              single_opinion = Opinion()
              for key, value in opinion.item():
                  setattr(single_opinion, key, value)
              self.opinions.append(single_opinion)


    def import_info(self):
       with open(f"./app/data/products/{self.product_id}.json","r", encoding="UTF-8") as jf:
          info = json.load(jf)
       self.product_name = info["product_name"]
       self.stats = info["stats"]


    def analyze(self):
      opinions = pd.DataFrame.from_dict([opinion.transform_to_dict()for opinion in self.opinions])
      self.stats["opinions_count"] = opinions.shape[0]
      self.stats["pros_count"] = opinions.pros_pl.astype(bool).sum()
      self.stats["cons_count"] = opinions.cons_pl.astype(bool).sum()
      self.stats["pros_cons_count"] = opinions.apply(lambda o: bool(o.pros_pl) and bool(o.cons_pl), axis=1).sum()





class Opinion:
    selectors = {
        "opinion_id": (None, "data-entry-id"),
        "author": ("span.user-post__author-name",),
        "recommendation": ("span.user-post__author-recomendation > em",),
        "stars": ("span.user-post__score-count",),
        "content_pl": ("div.user-post__text",),
        "pros_pl": ("div.review-feature__item--positive", None, True),
        "cons_pl": ("div.review-feature__item--negative", None, True),
        "vote_yes": ("button.vote-yes","data-total-vote"),
        "vote_no": ("button.vote-no","data-total-vote"),
        "published": ("span.user-post__published > time:nth-child(1)","datetime"),
        "purchased": ("span.user-post__published > time:nth-child(2)","datetime"),
    }

    def __init__(self, opinion_id, author, recommendation, stars, content, pros, cons, vote_yes, vote_no, publish_date, purchase_date):
        self.opinion_id = opinion_id
        self.author = author
        self.recommendation = recommendation
        self.stars = stars
        self.content = content
        self.pros = pros
        self.cons = cons
        self.vote_yes = vote_yes
        self.vote_no = vote_no
        self.publish_date = publish_date
        self.purchase_date = purchase_date
    
    def __str__(self):
        return "\n".join([f"{key}: {getattr(self, key)}" for key in self.selectors.keys()])
    
    def __repr__(self):
        return "Opinion("+", ".join([f"{key}={str(getattr(self, key))}" for key in self.selectors.keys()])+")"
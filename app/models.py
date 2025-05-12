class Product:
    def __init__(self):
        pass

class Opinion:
    def __init__(self, opinion_id, author, recommendation, stars, content, pros, cons, vote_yes, vote_no, publish_date, purchase_date):
        self.opinion_id = opinion_id
        self.author = author
        self.recommendation = recommendation
        self.stars = stars 
        self.pros = pros
        self.cons = cons
        self.vote_yes = vote_yes
        self.vote_no = vote_no
        self.publish_date = publish_date
        self.purchase_date = purchase_date
    
    def __str__(self):
        return "\n".join(f"{key} : {getattr(self,key)}" for key in self.seletors.keys())

    def __repr__(self):
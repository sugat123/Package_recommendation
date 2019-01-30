# Importing Libraries and cookbooks
from recsys import * ## recommender system cookbook
from generic_preprocessing import * ## pre-processing code
from IPython.display import HTML ## Setting display options for Ipython Notebook

# Importing rating data and having a look
ratings = pd.read_csv('ratings.csv')
#ratings = pd.DataFrame(df,columns=['UserId','PackageId','Rating','timestamp'])


# Importing movie data and having a look at first five columns
packages = pd.read_csv('packages.csv')
#packages = pd.DataFrame(d,columns=['ID','title','Duration'])
#packages.columns = ['ID','title','Duration']


# Creating interaction matrix using rating data
interactions = create_interaction_matrix(df = ratings,
                                         user_col = 'UserId',
                                         item_col = 'PackageId',
                                         rating_col = 'Rating')

interactions_history = create_interaction_matrix(df = ratings,
                                         user_col = 'UserId',
                                         item_col = 'PackageId',
                                         rating_col = 'timestamp')

# Create User Dict
user_dict = create_user_dict(interactions=interactions)
user_dict_history = create_user_dict(interactions=interactions_history)
# Create Item dict
packages_dict = create_item_dict(df = packages,
                               id_col = 'ID',
                               name_col = 'title')

mf_model = runMF(interactions = interactions,
                 n_components = 30,
                 loss = 'warp',
                 epoch = 30,
                 n_jobs = 4)

mf_model = runMF(interactions = interactions_history,
                 n_components = 30,
                 loss = 'warp',
                 epoch = 30,
                 n_jobs = 4)
## Calling 10 movie recommendation for user id 2
rec_list = sample_recommendation_user(model = mf_model, 
                                      interactions = interactions, 
                                      user_id = 2, 
                                      user_dict = user_dict,
                                      item_dict = packages_dict, 
                                      threshold = 4,
                                      nrec_items = 5,
                                      show = True)

rec_list_history = sample_recommendation_user(model = mf_model, 
                                      interactions = interactions_history, 
                                      user_id = 2, 
                                      user_dict = user_dict_history,
                                      item_dict = packages_dict, 
                                      threshold = 4,
                                      nrec_items = 5,
                                      show = True)
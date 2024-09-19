import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_query(query):
    headers = {"Content-Type": "application/json"}
    response = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

new_query = """{
  playerLevels {
    level
    exp
  }
}"""

result = run_query(new_query)
df = pd.DataFrame(result['data']['playerLevels'])

table_data = df[['level', 'exp']]
table = plt.table(cellText=df.values,
                  colLabels=df.columns,
                  colWidths=[0.15]*len(df.columns),
                  cellLoc='right',
                  loc='top',
                  bbox=[0.15, -0.4, 0.2, 0.3])

# Adjust the layout
plt.subplots_adjust(left=0.1, bottom=0.3)


sns.lineplot(x="level", y="exp", data=df)

plt.title('Player Levels vs Experience')
plt.xlabel('Level')
plt.ylabel('Experience')
plt.show()

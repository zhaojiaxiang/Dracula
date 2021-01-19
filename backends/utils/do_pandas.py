import pandas as pd

# x = [x for x in range(100)]

# x = [[x for x in range(100)] for i in range(70000)]

x = [[x for x in range(10)] for i in range(100)]

y = [[y for y in range(100)] for j in range(100)]


# l = [[1,2,3,4,5], [6,7,8,9,0], [1,3,5,7,9], [2,4,6,8,0]]

df=pd.DataFrame(x)
# df = df.transpose()

df1 = pd.DataFrame(y)
# df1 = df.transpose()

# df.to_excel('b.xlsx', sheet_name='Sheet1', index = False,header = False)
# df1.to_excel('b.xlsx', sheet_name='Sheet2', index = False,header = False)

with pd.ExcelWriter('789.xlsx') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False, header=False)
    df1.to_excel(writer, sheet_name='Sheet2', index=False, header=False)

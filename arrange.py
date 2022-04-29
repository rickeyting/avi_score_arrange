

def arrange_raw_data():
    df = pd.read_csv(r'C:\Users\A2433\Desktop\873\20220406_sp.csv')
    
    threshold_dict = {'D001': 0.78, 'D002': 0.84, 'D003': 0.84, 'D004': 0.92, 'D005': 0.87, 'D006': 0.84, 'D007': 0.89, 'D008': 0.9, 'D009': 0.86, 'D010': 0.85, 'D011': 0.89, 'D012': 0.86,'D013': 0.87, 'D014': 0.8}
    types = ['D001','D002','D003','D004','D005','D006','D007','D008','D009','D010','D011','D012','D013','D014']
    
    for i in range(1,15):
        df.loc[df['AI'] == i, 'AI'] = types[i-1]
        df.loc[df['VRS'] == i, 'VRS'] = types[i-1]
    df['max'] = df[types].idxmax(axis=1)
    df['multi'] = df['max']
    for i in threshold_dict:
        df.loc[(df['max']==i) & (df['D000'] > threshold_dict[i]), 'multi'] = 'D000'
    df.loc[df['ok'] > 0.82, 'binary'] = 'OK'
    df.loc[df['ok'] <= 0.82, 'binary'] = 'NG'
    df['result'] = df['binary']
    df.loc[df['result'] == 'NG', 'result'] = df.loc[df['result'] == 'NG', 'max']
    df.loc[(df['result'] == 'OK') & (df['multi'] != 'D000'), 'result'] = df.loc[(df['result'] == 'OK') & (df['multi'] != 'D000'), 'multi']
    df.loc[df['result'] == 'OK', 'result'] = 'D000'
    df.to_csv(r'C:\Users\A2433\Desktop\873\20220406_sp.csv', index=False)
    
    for i in tqdm(df.loc[df['result'] != df['AI']].index.values.tolist()):
        col = df.at[i,'result']
        origin = df.at[i,'D000']
        current = random.uniform(threshold_dict[col],1)
        df.loc[df.index == i, 'D000'] = current
        change = 1 - current
        summ = df.loc[df.index == i,types].sum(axis=1)
        change = change / summ
        for j in types:
            df.loc[df.index == i,j] = df.loc[df.index == i,j]*change
        df.loc[(df.index == i) & (df.ok < 0.82), 'ok'] = random.uniform(0.82,1)
    '''
    for i in types:
        score = df.loc[df['VRS'] == i, 'ok'].values.tolist()  
        df.loc[df['VRS'] == i, 'D000'] = random.sample(score,len(score))
    '''
    df['max_value'] = df[types].max(axis = 1)
    df['sum'] = df[['D000'] + types].sum(axis = 1)
    df['rest'] = 1 - df['sum']
   
    '''
    for i in types:
        for j in tqdm(df.loc[(df['VRS'] == i) & (df['AI'] != i)].index.values.tolist()):
            df.loc[(df.index == j) & (df[i] < 0.4), j] = random.uniform(0, 0.4)
    '''
    df.to_csv(r'C:\Users\A2433\Desktop\873\20220406_sp.csv', index=False)
    
    
def hist_plot_z01(path):
    df = pd.read_csv(path)
    types = ['D001','D002','D003','D004','D005','D006','D007','D008','D009','D010','D011','D012','D013','D014']
    for i in types:
        print(i)
        right = df.loc[df['VRS'] == i, i]
        left = df.loc[df['VRS'] != i, i]
        
        right_mean = round(right.mean(),2)
        right_std = round(right.std(),2)
        right_sigma = right_mean - 4*right_std
        right_min = np.min(right)
        print(right_min)
        left_mean = round(left.mean(),2)
        left_std = round(left.std(),2)
        left_sigma = left_mean + 4*left_std
        left_max = np.max(left)
        print(left_max)
        for j in range(2):
            if j == 0:
                fig, ax = plt.subplots()
                plt.hist(right,bins=50)
                plt.plot([right_sigma,right_sigma], [0,100], 'b--', linewidth = 0.7)
                ax.text(right_sigma, 200, "{}_4σ:{:.2f}".format(TYPE_DIC[types.index(i)+1], right_sigma), ha="left", color='blue')
                plt.plot([right_min,right_min], [0,100], '--',color='blueviolet', linewidth = 0.7)
                ax.text(right_min, 600, "{}_min:{:.2f}".format(TYPE_DIC[types.index(i)+1], right_min), ha="left", color='blueviolet')
                plt.xlim(0, 1)
                plt.ylim(0, 200)
                plt.show()
            else:
                fig, ax = plt.subplots()
                plt.hist(left,bins=50,color='orange')
                plt.plot([left_sigma,left_sigma], [0,100], 'r--', linewidth = 0.7)
                ax.text(left_sigma, 20000, "other_4σ:{:.2f}".format(left_sigma), ha="left", color='red')
                plt.plot([left_max,left_max], [0,100], '--',color='firebrick', linewidth = 0.7)
                ax.text(left_max, 40000, "other_max:{:.2f}".format(left_max), ha="right", color='firebrick')
                plt.xlim(0, 1)
                #plt.ylim(0, 50000)
                plt.show()

        fig, ax = plt.subplots()
        sns.distplot(right,bins=50, ax=ax, label='{}'.format(TYPE_DIC[types.index(i)+1]), kde_kws={'bw_adjust':2})
        sns.distplot(left,bins=50, ax=ax, label='Other classification', kde_kws={'bw_adjust':2})
        plt.plot([right_sigma,right_sigma], [0,100], 'b--', linewidth = 0.7)
        plt.plot([left_sigma,left_sigma], [0,100], 'r--', linewidth = 0.7)
        ax.text(right_sigma, 20, "{}_4σ:{:.2f}".format(TYPE_DIC[types.index(i)+1], right_sigma), ha="left", color='blue')
        ax.text(left_sigma, 30, "other_4σ:{:.2f}".format(left_sigma), ha="left", color='red')
        plt.plot([right_min,right_min], [0,100], '--',color='blueviolet', linewidth = 0.7)
        plt.plot([left_max,left_max], [0,100], '--',color='firebrick', linewidth = 0.7)
        ax.text(right_min, 60, "{}_min:{:.2f}".format(TYPE_DIC[types.index(i)+1], right_min), ha="left", color='blueviolet')
        ax.text(left_max, 65, "other_max:{:.2f}".format(left_max), ha="right", color='firebrick')
        
        plt.xlim(0, 1)
        plt.ylim(0, 100)
        plt.legend(bbox_to_anchor=(1.02, 1.0), loc='upper left', fontsize = 12)
        textstr = '\n'.join((
            r'Mean   StDEV     N',
            r'$%.2f$    $%.2f$        $%.0f$' % (right_mean,right_std,len(right), ),
            r'$%.2f$    $%.2f$        $%.0f$' % (left_mean,left_std,len(left), ),
            ))
        props = dict(boxstyle='round', alpha=0.5, facecolor='white')
        ax.text(1.05, 0.75, textstr, transform=ax.transAxes, fontsize=12,
                verticalalignment='top', bbox=props)
        #plt.savefig('{}.png'.format(title), dpi = 200,bbox_inches='tight')
        plt.show()

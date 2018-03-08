import scipy.stats as stats
#make sure to change the numbers in the table
contingency_table = [ [ 20, 6], [43,8] ]
oddsratio, pvalue = stats.fisher_exact(contingency_table)
print "odds ratio: ", oddsratio, "p value is: ", pvalue
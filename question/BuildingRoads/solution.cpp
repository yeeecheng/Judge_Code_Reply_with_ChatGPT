#include<iostream>
#include<algorithm>
#include<vector>
#include<set>
#include<stack>
#include<unordered_map>
#include<map>
#include<unordered_set>
#include<string>
#include<cmath>
#include<stack>
#include<queue>
#include<regex>
using namespace::std;
 
inline int read() {
	int x = 0; bool f = 0; char ch = getchar();
	while (ch < '0' || '9' < ch)f |= ch == '-', ch = getchar();
	while ('0' <= ch && ch <= '9')x = x * 10-'0' + ch, ch = getchar();
	return f ? -x : x;
}
 
void dfs(vector<vector<int>>& mp, vector<bool>& found, int curr) {
	found[curr] = true;
	for (int x : mp[curr]) {
		if (found[x] == false) {
			dfs(mp, found, x);
		}
	}
}
 
int main() {
	int n = read(), m = read();
	vector<vector<int>>mp(n + 1);
	vector<bool> found(n + 1);
	vector<int>ret;
	for (int i = 0; i < m; ++i) {
		int k = read(), l = read();
		mp[k].push_back(l);
		mp[l].push_back(k);
	}
	for (int i = 1; i <= n; ++i) {
		if (found[i] == false) {
			ret.push_back(i);
			dfs(mp, found, i);
		}
	}
	cout << (ret.size() - 1) << '\n';
	for (int i = 1; i < ret.size(); ++i) {
		cout << ret[i] << ' ' << ret[i - 1] << '\n';
 
	}
}
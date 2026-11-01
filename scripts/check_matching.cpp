// Exact checker B: polygon-flip graph, incidence multiplicities and edge domination.
#include <fstream>
#include <iostream>
#include <set>
#include <vector>
#include <stdexcept>
#include <algorithm>
using namespace std;
void require(bool x,const char*s){if(!x)throw runtime_error(s);}
int main(int argc,char**argv){try{
 require(argc==3,"usage: checker polygon-graph.txt matching.txt");ifstream g(argv[1]),m(argv[2]);
 int n,e;require(bool(g>>n>>e)&&n==429&&e==1287,"graph dimensions");
 vector<pair<int,int>> edges;set<pair<int,int>> unique;vector<int>degree(n),incident(n);
 for(int i=0;i<e;i++){int a,b;require(bool(g>>a>>b)&&0<=a&&a<n&&0<=b&&b<n&&a!=b,"bad graph edge");if(a>b)swap(a,b);require(unique.emplace(a,b).second,"duplicate graph edge");edges.emplace_back(a,b);degree[a]++;degree[b]++;}
 string extra;require(!(g>>extra),"trailing graph data");for(int d:degree)require(d==6,"wrong degree");
 int k;require(bool(m>>k)&&0<=k&&k<=214,"matching size");
 for(int i=0;i<k;i++){int a,b;require(bool(m>>a>>b)&&0<=a&&a<n&&0<=b&&b<n&&a!=b,"bad matching pair");if(a>b)swap(a,b);require(unique.count({a,b}),"nonedge");incident[a]++;incident[b]++;}
 require(!(m>>extra),"trailing matching data");for(int x:incident)require(x<=1,"endpoint collision");
 for(auto [a,b]:edges)require(incident[a]+incident[b]>=1,"undominated edge: not maximal");
 cout<<"{\"verdict\":\"PASS\",\"matching_size\":"<<k<<",\"unmatched_vertices\":"<<n-2*k<<",\"edge_domination_checked\":"<<e<<"}"<<endl;
 }catch(const exception&e){cerr<<"FAIL "<<e.what()<<endl;return 1;}return 0;}

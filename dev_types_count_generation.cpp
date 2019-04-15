#include <bits/stdc++.h>
using namespace std;

int main() {
	string s;

	while (getline(cin, s)) {
		cout << "SELECT developer_type, (total_product_manager * 100) / total_developers as percentage_product_manager\n";
		cout << "FROM (SELECT '"<< s << "' as developer_type, COUNT(Respondent) as total_product_manager\n";
    	cout << "FROM `third-diorama-233818.1.survey_results_public`\n";
	    cout << "WHERE LOWER(DevType) LIKE LOWER('%" << s << "%')),\n"; 
	    cout << "(SELECT COUNT(Respondent) as total_developers\n";
	    cout << "FROM `third-diorama-233818.1.survey_results_public`)\n";
	    cout << '\n';
	    cout << "UNION ALL\n\n";
	}
}

#include <iostream>
#include <fstream>
#include <cstring>
#include <assert.h>

#include <boost/property_tree/xml_parser.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/foreach.hpp>

using namespace std;

using boost::property_tree::ptree;


class Counter
{
private:
	int cnt;
public:
	Counter():cnt(0){}

	void increment()
	{
		++cnt;
	}

	int getValue()
	{
		return cnt;
	}
};

class DumbXMLParser
{
private:
	const string FAIL = "----FAIL----";
public:
	void processXMLData(const string path, Counter &counter)
	{
		ptree pt;
		ifstream file(path);
		read_xml(file, pt);
		BOOST_FOREACH(ptree::value_type const &v, pt.get_child("graph"))
		{
			if(v.first == "node")
			{
				BOOST_FOREACH(ptree::value_type const &node, v.second.get_child(""))
				{
					if(node.first == "<xmlattr>"){
						string id   = node.second.get<string>("id"  , FAIL);
						string name = node.second.get<string>("name", FAIL);
						assert(id   != FAIL);
						assert(name != FAIL);
						cout << "I found a node with id " << id << ", and name " << name << endl;
						counter.increment();
					}
				}
			}
		}
		BOOST_FOREACH(ptree::value_type const &v, pt.get_child("graph"))
		{
			if(v.first == "edge")
			{
				BOOST_FOREACH(ptree::value_type const &node, v.second.get_child(""))
				{
					if(node.first == "<xmlattr>"){
						string id     = node.second.get<string>("id"    , FAIL);
						string source = node.second.get<string>("source", FAIL);
						string target = node.second.get<string>("target", FAIL);
						assert(id     != FAIL);
						assert(source != FAIL);
						assert(target != FAIL);
						cout << "There is an edge with id " << id << " from " << source << " to " << target << endl;
					}
				}
			}
		}

	}
};

int main()
{
	string path = "graph.xml";
	Counter myCounter;

	DumbXMLParser constructor;
	constructor.processXMLData(path, myCounter);

	cout << endl << "Number of counted nodes: " << myCounter.getValue() << endl;
}

function out = DumbXMLParser2()
xmlfile = 'graph.xml';
xml = xmlread(xmlfile);
children = xml.getChildNodes;
graph = children.item(0);
data = graph.getChildNodes;
for i=1:data.getLength
    entry = data.item(i-1);
    if (strcmp(entry.getNodeName,'node'))
        %Knoten gefunden
        id = char(entry.getAttributes.item(0).getValue);
        name = char(entry.getAttributes.item(1).getValue);
        fprintf('I found a node with id %s and name %s\n',id,name);
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %                                                                      %
        %               Hier eventuell eigenen Code einfügen                   %
        %                                                                      %
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                
    end;
    if (strcmp(entry.getNodeName,'edge'))
        %Kante gefunden
        id = char(entry.getAttributes.item(0).getValue);
        source = char(entry.getAttributes.item(1).getValue);
        target = char(entry.getAttributes.item(2).getValue);
        fprintf('There is an edge with id %s from %s to %s\n',id,source,target);
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %                                                                      %
        %               Hier eventuell eigenen Code einfügen                   %
        %                                                                      %
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
    end;
end;

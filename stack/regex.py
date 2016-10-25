import re

"""
v1:
private String convertNameToId(String name) {
 -    name = Normalizer.normalize(name, Normalizer.Form.NFD);
 -    name = name.replaceAll("[^\\p{ASCII}]", "");
 -    return name.toLowerCase().replaceAll(" ", "_");
 -  }

v2:
public String convertNameToId(String name) {
    name = Normalizer.normalize(name, Normalizer.Form.NFD);
    name = name.replaceAll("[^\\p{ASCII}]", "");
    return name.toLowerCase()
        .replaceAll(" ", "_")
        .replaceAll("#", "_")
        .replaceAll("\\/", "_")
        .replaceAll("\\.", "");
  }
"""

# p{ASCII}	-> All ASCII:[\x00-\x7F]


tech_name = 'Angular JS'
print re.sub('[#/ ]', '_', re.sub('[^\x00-\x7F]', '_', re.sub('[.]', '', tech_name.lower())))

tech_name = 'Apache Axis2/Java'
print re.sub('[#/ ]', '_', re.sub('[^\x00-\x7F]', '_', re.sub('[.]', '', tech_name.lower())))

tech_name = 'PL-SQL'
print re.sub('[#/ ]', '_', re.sub('[^\x00-\x7F]', '_', re.sub('[.]', '', tech_name.lower())))

tech_name = 'subversion_(svn)'
print re.sub('[#/ ]', '_', re.sub('[^\x00-\x7F]', '_', re.sub('[.]', '', tech_name.lower())))

tech_name = 'VB .Net'
print re.sub('[#/ ]', '_', re.sub('[^\x00-\x7F]', '_', re.sub('[.]', '', tech_name.lower())))
print re.sub('[#/ ]', '_', re.sub('[^\x00-\x7F]', '_', tech_name.lower()))

tech_name = 'CI&T Andon'
print re.sub('[#/ ]', '_', re.sub('[^\x00-\x7F]', '_', re.sub('[.]', '', tech_name.lower())))

# expected 
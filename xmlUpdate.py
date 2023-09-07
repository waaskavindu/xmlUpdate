import xml.etree.ElementTree as ElementTree

import difflib

def getData(jarName,xml_filename,validationRun):
    try:
    # Parse the XML file
        tree = ElementTree.parse(xml_filename)
        root = tree.getroot()

        # Find the element you want to update using the element_path
        element_data = root.findall("*/application/")

        #print(element_data)
        for application in root.findall('*/application'):
            jar = application.find('jar').text
            if (jar == jarName) :
                name = application.find('name').text
                version = application.find('version').text
                version_element = application.find('version')
                if validationRun:
                    print("Version Validation : ",version)
                    break
                else:
                    print("\n Client name : ",jar,"\n Initial version : ",version)
                    new_value=countIncrease(version)

                    # Update the element
                    version_element.text = str(new_value)  # Replace with new value

                    # Save the updated XML back to the file
                    tree.write(xml_filename)
                    print(f"Updated version to: {new_value}")
                    break

    except ElementTree.ParseError as e:
        print(f"Error parsing the XML file: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
def countIncrease(value):
    # Split the count into segments
    segments = value.split(".")
    last_segment = str(int(segments[-1]) + 1)
    segments[-1] = last_segment
    new_value = ".".join(segments)
    return new_value

def readFiles(fileName):
    data = {}
    # Open the file in read mode
    with open(fileName, 'r') as file:
        for line in file:
            
            parts = line.split('=')
        
            if len(parts) == 2:
            
                key = parts[0].strip()
                value = parts[1].strip()
                data[key] = value
        return data

def validation(releasevalue):
    getData(releasevalue,xml_filename,True)

if __name__ == "__main__":
    xml_filename = "agent.xml" 
    element_path = "*/application/version" 
   
    releasebuilds = readFiles("releasebuilds") # store jar names which needed to update
    
    for releasekey, releasevalue in releasebuilds.items():
        getData(releasevalue,xml_filename,False)
        validation(releasevalue)



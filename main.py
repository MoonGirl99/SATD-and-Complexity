import argparse
import pandas as pd
from pydriller import Repository
import lizardsatd
import lizard
import os
import re

# Implemented by Mahshid


# Function to get complexity of a file
def get_complexity(filename, source):
    analyze_file = lizard.FileAnalyzer(lizard.get_extensions([lizardsatd.LizardExtension()]))
    result = analyze_file.analyze_source_code(filename, source)

    return result


# Function to extract SATD comments from a file
def extract_satd_comments(filepath):
    satd_comments = []
    with open(filepath) as f:
        contents = f.read()
        # Match SATD comments using regular expression
        matches = re.findall(r"\/\/.*?(?:TODO|FIXME|HACK|XXX|BUG|ISSUE|hack|retarded|at a loss|stupid|remove this code|ugly|take care|something's gone wrong|nuke|is problematic|may cause problem|hacky|unknown why we ever experience this|treat this as a soft error|silly|workaround for bug|kludge|fixme|this isn't quite right|trial and error|give up|this is wrong|hang our heads in shame|temporary solution|causes issue|something bad is going on|cause for issue|this doesn't look right|is this next line safe|this indicates a more fundamental problem|temporary crutch|this can be a mess|this isn't very solid|this is temporary and will go away|is this line really safe|there is a problem|some fatal error|something serious is wrong|don't use this|get rid of this|doubt that this would work|this is bs|give up and go away|risk of this blowing up|just abandon it|prolly a bug|probably a bug|hope everything will work|toss it|barf|something bad happened|fix this crap|yuck|certainly buggy|remove me before production).*?\n", contents, re.IGNORECASE)
        satd_comments += matches
    return satd_comments


# Main function
def main():
    result = []
    satd_comments = []
    resultsatd = []
    increase = 0
    decrease = 0
    # Define the repository URL

    repo_url = "https://github.com/apache/commons-net"


    # Define the path to your repository directory here
    repo_path = '/home/mahshid/non-default files/MiningSW1_/miningsw1'


    # Define the file extensions you want to search for here
    extensions = ['.java']


    # Start: Using the Lizard library to analyze a file for self-admitted technical debt (SATD) comments///////
    analyze_file = lizard.FileAnalyzer(lizard.get_extensions([lizardsatd.LizardExtension()]))
    # End

    # Start: Listing the Java files of the repository
    for root, dirs, files in os.walk(repo_path):

        """ 
        This loop provides a path to find 
        all java files in repository path
        """
        for file in files:
            # Check if the file has a Java file extension
            if any(file.endswith(ext) for ext in extensions):
                result.append({
                    'file_name': file
                })

    # End of finding Java files


            # Start: Extract the cyclomatic complexity for the methods of the file
                file_path = os.path.join(root, file)
                newresult = analyze_file(file_path)
    
                for func in newresult.function_list:    
                    
                    print('\t\tFunction:', func.name)
                    print('\t\tComplexity:', func.cyclomatic_complexity)
            # End of extracting cyclomatic complexity

                    # Start: Extract the SATD comments for the file

                    satd_comments = extract_satd_comments(file_path)
                    print('\t\tSATD comments:', satd_comments)
                    
                    resultsatd.append({
                        'function_name': func.name,
                        'complexity': float(func.cyclomatic_complexity),
                        'satd_number': float(len(satd_comments))
                    })
                    # End of extracting SATD comments
                
                    
    print(resultsatd)
    st = pd.DataFrame(resultsatd, columns= ['file_name', 'function_name', 'complexity', 'satd_number'])
    st.to_csv('satd.csv', index=False)
    

    # Use PyDriller to iterate over the commits in the repository
    for commit in Repository('https://github.com/apache/commons-net', only_modifications_with_file_types=['.java']).traverse_commits():

        
        for modified in commit.modified_files:
            if modified.source_code and modified.source_code_before and modified.filename.endswith(".java"):             

                # Get the complexity of the file
                Complexity1 = get_complexity(modified.filename, modified.source_code)
                Complexity2 = get_complexity(modified.filename, modified.source_code_before)

                # Compare the complexity of the file before and after the commit
                if Complexity1.average_cyclomatic_complexity == Complexity2.average_cyclomatic_complexity:
                    continue
                else:
                    diff1 = Complexity1.average_cyclomatic_complexity - Complexity2.average_cyclomatic_complexity
                    print("difference", diff1)
                    if diff1 > 0:
                        increase = diff1
                    
                    elif diff1 <= 0:
                        decrease = diff1

                    # Save the result in a list
                        
                    result.append({
                        'commit_hash': commit.hash,
                        'commit_msg': commit.msg,
                        'complexity': modified.complexity,
                        'Complexity_done': float(Complexity1.average_cyclomatic_complexity),
                        'Complexity_before': float(Complexity2.average_cyclomatic_complexity),
                        'satd_increase_complexity_change': increase,
                        'satd_decrease_complexity_change': decrease
                    })
                    
    # Save the result in a csv file    
    df = pd.DataFrame(result, columns= ['commit_hash', 'commit_msg', 'complexity','Complexity_done', 'Complexity_before', 'satd_increase_complexity_change', 'satd_decrease_complexity_change'])
    df.to_csv("final.csv", index=False)

# Implemented by Mahshid
if __name__ == '__main__':
    main()

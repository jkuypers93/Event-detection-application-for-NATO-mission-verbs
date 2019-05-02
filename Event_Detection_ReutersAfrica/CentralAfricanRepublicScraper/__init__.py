import pandas as pd
from utils import stem_mission_verbs, mapping_data, process_coordinates
from analyze import filter_and_analyze_content


def main():
    
    with open("NATO_Mission_Verbs.txt", "r") as mission_verbs_file:
        mission_verbs = mission_verbs_file.readlines()
    
    stemmed_mission_verbs = stem_mission_verbs(mission_verbs)
    
    content_df_raw = pd.read_csv('ReutersAfrica_TopStoriesRSSFeed_List.csv', 
                     header=None)
    
    analyzed_content, nr_detected = filter_and_analyze_content(
            content_df_raw, stemmed_mission_verbs)


    analyzed_content_coordinates = process_coordinates(analyzed_content)

    analyzed_content_coordinates.to_csv('ReutersAfrica_Analysed.csv')
    
    print("\nAnalysis was succesful! \n%i articles were detected \nResults can be found in ReutersAfrica_Analysed.csv" 
          %(nr_detected))



if __name__ == "__main__":
    
    main()
INSERT_SQL = "INSERT INTO ocr_llm_analysis_result (serial_no,ocr_result,llm_result,json_result,analyze_time,time_cost) VALUES (%s,%s,%s,%s,%s,%s)"
SELECT_ALL = "SELECT count(1) as count_all FROM ocr_llm_analysis_result"
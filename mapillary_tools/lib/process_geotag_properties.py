import processing


def process_geotag_properties(import_path,
                              geotag_source,
                              video_duration,
                              sample_interval,
                              video_start_time,
                              use_gps_start_time,
                              duration_ratio,
                              rerun,
                              offset_time=0.0,
                              local_time=False,
                              interval=0.0,
                              geotag_source_path=None,
                              offset_angle=0,
                              timestamp_from_filename=False,
                              verbose=False):

    # get list of file to process
    process_file_list = processing.get_process_file_list(import_path,
                                                         "geotag_process",
                                                         rerun,
                                                         verbose)
    if not len(process_file_list):
        if verbose:
            print("No images to run geotag process")
            print("If the images have already been processed and not yet uploaded, they can be processed again, by passing the argument --rerun")
        return

    # sanity checks
    if geotag_source_path == None and geotag_source != "exif":
        # if geotagging from external log file, path to the external log file
        # needs to be provided, if not, exit
        print("Error, if geotagging from external log, rather than image EXIF, you need to provide full path to the log file.")
        processing.create_and_log_process_in_list(process_file_list,
                                                  import_path,
                                                  "geotag_process"
                                                  "failed",
                                                  verbose)
        return

    elif geotag_source != "exif" and not os.path.isfile(geotag_source_path):
        print("Error, " + geotag_source_path +
              " file source of gps/time properties does not exist. If geotagging from external log, rather than image EXIF, you need to provide full path to the log file.")
        processing.create_and_log_process_in_list(process_file_list,
                                                  import_path,
                                                  "geotag_process"
                                                  "failed",
                                                  verbose)
        return

    # function calls
    if geotag_source == "exif":
        geotag_properties = processing.geotag_from_exif(process_file_list,
                                                        import_path,
                                                        offset_angle,
                                                        verbose)
    elif geotag_source == "gpx":
        geotag_properties = processing.geotag_from_gpx(process_file_list,
                                                       import_path,
                                                       geotag_source_path,
                                                       offset_time,
                                                       offset_angle,
                                                       local_time,
                                                       interval,
                                                       timestamp_from_filename,
                                                       video_duration,
                                                       sample_interval,
                                                       video_start_time,
                                                       use_gps_start_time,
                                                       duration_ratio,
                                                       verbose)
    elif geotag_source == "csv":
        geotag_properties = processing.geotag_from_csv(process_file_list,
                                                       import_path,
                                                       geotag_source_path,
                                                       offset_time,
                                                       offset_angle,
                                                       verbose)
    else:
        geotag_properties = processing.geotag_from_json(process_file_list,
                                                        import_path,
                                                        geotag_source_path,
                                                        offset_time,
                                                        offset_angle,
                                                        verbose)

<?php

// if set to 0 will attempt to find all images currently stored
$GET_LATEST = 1;
// echo PHP_EOL.PHP_EOL.PHP_EOL.PHP_EOL.PHP_EOL.'SCRAPE NOAA GO > '.date('r').PHP_EOL.PHP_EOL.PHP_EOL.PHP_EOL.PHP_EOL;

$DATA_FOLDER = '/var/www/html/projects/noaa/scraped/';
$DATA_CSV = 'scraped-data.csv';
$URL = 'https://www.ndbc.noaa.gov/images/buoycam/';

function timer()
{
    static $startTIME;

    if (is_null($startTIME)) {
        $startTIME = microtime(true);
    } else {
        $diff = round((microtime(true) - $startTIME), 4);
        $startTIME = null;

        return $diff;
    }
}

function convertToKnots($wind_ms)
{
    return (float) $wind_ms * 1.943844;
}

function getBeaufortForceFromWind($windFloat)
{
    $knots = convertToknots($windFloat);

    if ($knots < 1) {
        return 0;
    } elseif ($knots < 4) {
        return 1;
    } elseif ($knots < 7) {
        return 2;
    } elseif ($knots < 11) {
        return 3;
    } elseif ($knots < 17) {
        return 4;
    } elseif ($knots < 22) {
        return 5;
    } elseif ($knots < 28) {
        return 6;
    } elseif ($knots < 34) {
        return 7;
    } elseif ($knots < 41) {
        return 8;
    } elseif ($knots < 48) {
        return 9;
    } elseif ($knots < 56) {
        return 10;
    } elseif ($knots < 64) {
        return 11;
    } elseif ($knots >= 64) {
        return 12;
    }
}

function getBeaufortForceFromWave($waveFloat)
{
    //#sea like mirror
    if ($waveFloat < .1) {
        return 0;
    }
    //# .1
    elseif ($waveFloat < .2) {
        return 1;
    }
    //# .2 - .3
    elseif ($waveFloat < .6) {
        return 2;
    }
    //# .6 - 1
    elseif ($waveFloat < 1) {
        return 3;
    }
    //# 1 - 1.5
    elseif ($waveFloat < 2) {
        return 4;
    }
    //# 2 - 2.5
    elseif ($waveFloat < 3) {
        return 5;
    }
    //# 3 - 4
    elseif ($waveFloat < 4) {
        return 6;
    }
    //# 4 - 5.5
    elseif ($waveFloat < 5.5) {
        return 7;
    }
    //# 5.5 - 7.5
    elseif ($waveFloat < 7.5) {
        return 8;
    }
    //# 7 - 10
    elseif ($waveFloat < 10) {
        return 9;
    }
    //# 9 - 12.5
    elseif ($waveFloat < 12.5) {
        return 10;
    }
    //# 11.5 - 16
    elseif ($waveFloat < 16) {
        return 11;
    }
    //# POSEIDON's WRATH
    elseif ($waveFloat >= 16) {
        return 12;
    }
}

function fillzero($text, $zeros = 2)
{
    return  str_pad($text, $zeros, '0', STR_PAD_LEFT);
}

// constructs the image url from the individual components
// Z92A_2019_04_10_0110.jpg
function constructImageUrl($station_code, $year, $month, $day, $hour, $minute)
{
    global $URL;

    return $URL.$station_code.'_'.$year.'_'.fillzero($month).'_'.fillzero($day).'_'.fillzero($hour).fillzero($minute).'.jpg';
}

// store the image and the data in the dataset
function saveImage($image)
{
    global $DATA_CSV, $DATA_FOLDER, $URL;

    $image_name = str_replace($URL, '', $image['image_url']);

    // PHP filesystem path normalization
    $csv_path = realpath($DATA_FOLDER.$DATA_CSV);
    $data = file_get_contents($csv_path);

    // check to make sure the image isn't already stored
    if (strpos($data, $image_name) !== false) {
        return false;
    }

    // only use the beaufort force from wind stat since wave data incomplete
    $new_data = $image_name.','.$image['data']['WSPD'].','.$image['data']['WVHT'].','.getBeaufortForceFromWind($image['data']['WSPD']);

    // concatenate data on the end of the string
    file_put_contents($csv_path, $data.PHP_EOL.$new_data);

    $image_path = str_replace($DATA_CSV, $image_name, $csv_path);
    file_put_contents($image_path, file_get_contents($image['image_url']));

    return true;
}

function getLatestImage($station_id, $station_code)
{
    // pull the last 5 days of data
    $log = @file_get_contents('https://www.ndbc.noaa.gov/data/5day2/'.$station_id.'_5day.txt');

    // fallback to the 45 day data set if 5 day data set doesn't exist.
    if ($log == false) {
        $log = @file_get_contents('https://www.ndbc.noaa.gov/data/realtime2/'.$station_id.'.txt');

        if ($log == false) {
            return 'ERROR: weather data not found';
        }
    }

    $log = explode("\n", $log);

    // get column headers; split by any whitespace
    $headers = preg_split('/\s+/', $log[0]);

    // remove the header information
    unset($log[0]);
    unset($log[1]);

    $count = 0;
    $since_last_image = 0;
    foreach ($log as $row) {
        $data = preg_split('/\s+/', $row);
        ++$count;

        $image_url = constructImageUrl($station_code, $data[0], $data[1], $data[2], $data[3], $data[4]);
        $file_headers = @get_headers($image_url);

        // if it's been too long since the last image, break out. You won't find more here.
        if ($since_last_image > 9) {
            break;
        }

        // skip if file doesn't exist
        if ($file_headers[0] == 'HTTP/1.1 404 Not Found') {
            ++$since_last_image;
            continue;
        }

        $since_last_image = 0;

        return [[
  'image_url' => $image_url,
  'data' => array_combine($headers, $data),
  ]];
    }

    return 'ERROR: image not found';
}

function getAllStoredImages($station_id, $station_code)
{
    // pull the last 5 days of data
    $log = @file_get_contents('https://www.ndbc.noaa.gov/data/5day2/'.$station_id.'_5day.txt');

    // fallback to the 45 day data set if 5 day data set doesn't exist.
    if ($log == false) {
        $log = @file_get_contents('https://www.ndbc.noaa.gov/data/realtime2/'.$station_id.'.txt');

        if ($log == false) {
            return 'ERROR: weather data not found';
        }
    }

    $log = explode("\n", $log);

    // get column headers; split by any whitespace
    $headers = preg_split('/\s+/', $log[0]);

    // remove the header information
    unset($log[0]);
    unset($log[1]);

    $count = 0;
    $since_last_image = 0;
    $images = [];
    foreach ($log as $row) {
        $data = preg_split('/\s+/', $row);
        ++$count;

        $image_url = constructImageUrl($station_code, $data[0], $data[1], $data[2], $data[3], $data[4]);
        $file_headers = @get_headers($image_url);

        // if it's been too long since the last image, break out. You won't find more here.
        if ($since_last_image > 9) {
            break;
        }

        // skip if file doesn't exist
        if ($file_headers[0] == 'HTTP/1.1 404 Not Found') {
            ++$since_last_image;
            continue;
        }

        $since_last_image = 0;

        $images[] = [
  'image_url' => $image_url,
  'data' => array_combine($headers, $data),
  ];
    }

    return $images;
}

/********************** MAIN **************************/

// echo '<pre>';

$buoycams = json_decode(file_get_contents('https://www.ndbc.noaa.gov/buoycams.php'));

foreach ($buoycams as $buoy) {
    if ($buoy->img == null) {
        continue;
    }

    // profiling for retriving image list
    timer();

    $station_code = explode('_', $buoy->img)[0];
    echo PHP_EOL.' > buoy #'.$buoy->id.' '.$station_code;

    if ($GET_LATEST == 1) {
        $images = getLatestImage($buoy->id, $station_code);
    } elseif ($GET_LATEST == 0) {
        $images = getAllStoredImages($buoy->id, $station_code);
    } else {
        die('$GET_LATEST must be 1 or 0');
    }

    echo ' ('.timer().'s)';

    echo PHP_EOL;

    // if there was an error display the error
    if (!is_array($images)) {
        echo $images.PHP_EOL;
        continue;
    }

    foreach ($images as $latest_image) {
        echo str_replace($URL, '', $latest_image['image_url'])."\t";
        if (isset($latest_image['image_url'])) {
            timer();
            if (saveImage($latest_image)) {
                echo 'Image stored.';
            } else {
                echo 'Image already stored.';
            }
            echo ' ('.timer().'s)';
            echo PHP_EOL;
        } else {
            echo $latest_image;
        }
    }
}

/*
 *  RPLIDAR
 *  Ultra Simple Data Grabber Demo App
 *
 *  Copyright (c) 2009 - 2014 RoboPeak Team
 *  http://www.robopeak.com
 *  Copyright (c) 2014 - 2016 Shanghai Slamtec Co., Ltd.
 *  http://www.slamtec.com
 *
 */
/*
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

#include <stdio.h>
#include <stdlib.h>

#include "rplidar.h" //RPLIDAR standard sdk, all-in-one header

#ifndef _countof
#define _countof(_Array) (int)(sizeof(_Array) / sizeof(_Array[0]))
#endif

#ifdef _WIN32
#include <Windows.h>
#define delay(x)   ::Sleep(x)
#else
#include <unistd.h>
static inline void delay(_word_size_t ms){
    while (ms>=1000){
        usleep(1000*1000);
        ms-=1000;
    };
    if (ms!=0)
        usleep(ms*1000);
}
#endif

//=======================BENCH 8 CAPSTONE CODE============================

#define QUALITY    0 // index of value in 2d array
#define ANGLE      1
#define DISTANCE   2
    
#define DATA_GOOD  1 // contants representing quality
#define DATA_BAD   0
#define DATA_INF   2

void printCondensedData(int nodes[][3], int len){ // for testing
  for (int pos=0; pos<len; pos++){
    printf("angle: %03d Dist: %6d Q: %d \n", 
           nodes[pos][ANGLE],
           nodes[pos][DISTANCE],
           nodes[pos][QUALITY]);
  }
}

void sendRPLidarData(int nodes[][3], int len){
  // TODO: send to relevant python script using MSI
  // printCondensedData(nodes, len); // for testing
  printf("[");
  for (int pos=0; pos<len; pos++){
    printf("(%d,%d,%d)", nodes[pos][QUALITY], nodes[pos][ANGLE], nodes[pos][DISTANCE]);
    if (pos != len-1) {printf(",");}
  }
  printf("]\n");
}


void printData(rplidar_response_measurement_node_t* nodes, size_t count){
  for (int pos = 0; pos < (int)count ; ++pos) {
    printf("%s theta: %03.2f Dist: %08.2f Q: %d \n", 
           (nodes[pos].sync_quality & RPLIDAR_RESP_MEASUREMENT_SYNCBIT) ?"S ":"  ", 
           (nodes[pos].angle_q6_checkbit >> RPLIDAR_RESP_MEASUREMENT_ANGLE_SHIFT)/64.0f,
           nodes[pos].distance_q2/4.0f,
           nodes[pos].sync_quality >> RPLIDAR_RESP_MEASUREMENT_QUALITY_SHIFT);
  }
}

void doWithData(rplidar_response_measurement_node_t* nodes, size_t count, int resolution){
  
  // condense data while still in c to reduce clock cycles
  
  int condensed[resolution][3]; // quality, angle, distance
   
  for (int i=0; i<resolution; i++){
    condensed[i][ANGLE] = i*360/resolution;
    condensed[i][DISTANCE] = 0;
    condensed[i][QUALITY] = DATA_BAD;
  }
  
  for (int pos = 0; pos < (int)count ; ++pos){
    int quality = nodes[pos].sync_quality >> RPLIDAR_RESP_MEASUREMENT_QUALITY_SHIFT;
    if (quality){
      int theta = (int)(nodes[pos].angle_q6_checkbit >> RPLIDAR_RESP_MEASUREMENT_ANGLE_SHIFT)/64;
      int bucket = theta/(360/resolution);
      int dis = (int)(nodes[pos].distance_q2);
      
      if (condensed[bucket][QUALITY] != DATA_GOOD || condensed[bucket][DISTANCE] > dis){
        condensed[bucket][DISTANCE] = dis;
        condensed[bucket][QUALITY] = DATA_GOOD;
      }
    }
  }
  
  sendRPLidarData(condensed, resolution);
}

//========================================================================

using namespace rp::standalone::rplidar;

bool checkRPLIDARHealth(RPlidarDriver * drv)
{
    u_result     op_result;
    rplidar_response_device_health_t healthinfo;


    op_result = drv->getHealth(healthinfo);
    if (IS_OK(op_result)) { // the macro IS_OK is the preperred way to judge whether the operation is succeed.
        printf("RPLidar health status : %d\n", healthinfo.status);
        if (healthinfo.status == RPLIDAR_STATUS_ERROR) {
            fprintf(stderr, "Error, rplidar internal error detected. Please reboot the device to retry.\n");
            // enable the following code if you want rplidar to be reboot by software
            // drv->reset();
            return false;
        } else {
            return true;
        }

    } else {
        fprintf(stderr, "Error, cannot retrieve the lidar health code: %x\n", op_result);
        return false;
    }
}

#include <signal.h>
bool ctrl_c_pressed;
void ctrlc(int)
{
    ctrl_c_pressed = true;
}

int main(int argc, const char * argv[]) {
    const char * opt_com_path = NULL;
    _u32         opt_com_baudrate = 115200;
    u_result     op_result;
    
    int          resolution = 8;

    printf("Ultra simple LIDAR data grabber for RPLIDAR.\n"
           "Version: "RPLIDAR_SDK_VERSION"\n");

    // replace:
    if (argc>1) resolution = atoi(argv[1]);

    // read serial port from the command line...
    // if (argc>1) opt_com_path = argv[1]; // or set to a fixed value: e.g. "com3" 

    // read baud rate from the command line if specified...
    // if (argc>2) opt_com_baudrate = strtoul(argv[2], NULL, 10);


    if (!opt_com_path) {
#ifdef _WIN32
        // use default com port
        opt_com_path = "\\\\.\\com3";
#else
        opt_com_path = "/dev/ttyUSB0";
#endif
    }

    // create the driver instance
    RPlidarDriver * drv = RPlidarDriver::CreateDriver(RPlidarDriver::DRIVER_TYPE_SERIALPORT);
    
    if (!drv) {
        fprintf(stderr, "insufficent memory, exit\n");
        exit(-2);
    }


    // make connection...
    if (IS_FAIL(drv->connect(opt_com_path, opt_com_baudrate))) {
        fprintf(stderr, "Error, cannot bind to the specified serial port %s.\n"
            , opt_com_path);
        goto on_finished;
    }

    rplidar_response_device_info_t devinfo;

	// retrieving the device info
    ////////////////////////////////////////
    op_result = drv->getDeviceInfo(devinfo);

    if (IS_FAIL(op_result)) {
        fprintf(stderr, "Error, cannot get device info.\n");
        goto on_finished;
    }

    // print out the device serial number, firmware and hardware version number..
    printf("RPLIDAR S/N: ");
    for (int pos = 0; pos < 16 ;++pos) {
        printf("%02X", devinfo.serialnum[pos]);
    }

    printf("\n"
            "Firmware Ver: %d.%02d\n"
            "Hardware Rev: %d\n"
            , devinfo.firmware_version>>8
            , devinfo.firmware_version & 0xFF
            , (int)devinfo.hardware_version);



    // check health...
    if (!checkRPLIDARHealth(drv)) {
        goto on_finished;
    }

	signal(SIGINT, ctrlc);
    
	drv->startMotor();
    // start scan...
    drv->startScan();

    // fetech result and print it out...
    while (1) {
        rplidar_response_measurement_node_t nodes[360*2];
        size_t   count = _countof(nodes);

        op_result = drv->grabScanData(nodes, count);

        if (IS_OK(op_result)) {
            drv->ascendScanData(nodes, count);
            doWithData(nodes, count, resolution);
        }

        if (ctrl_c_pressed){ 
			break;
		}
    }

    drv->stop();
    drv->stopMotor();
    // done!
on_finished:
    RPlidarDriver::DisposeDriver(drv);
    return 0;
}


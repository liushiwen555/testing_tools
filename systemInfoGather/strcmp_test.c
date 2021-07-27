#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <string.h>


int main() {
    clock_t start_time, end_time;
    double time_cost, total_time_cost, time_cost_avg, time_cost_max, time_cost_min;
    int result;
    double time_costs[20];
    char *str1 = "01234567890123456789";
    char *str2 = "0123456789012345678a";
    int time_count = 0;
    int time_costs_length = 20;
    int i;

    while (time_count++ < 20)
    {
        start_time = clock();
        for (i = 0; i < 2000000; i++)
        {
            result = strcmp(str1, str2);
        }
        end_time = clock();
        time_costs[time_count - 1] = (double)(end_time - start_time) / CLOCKS_PER_SEC;
    }

    // average
    double sum = 0;

    for (i = 0; i < time_costs_length; i++)
    {
        
        sum = sum + time_costs[i];
    }
    time_cost_avg = sum / 20;
    // max
    time_cost_max = time_costs[0];
    for (i = 0; i < time_costs_length; i++)
    {
        if (time_costs[i] > time_cost_max){
            time_cost_max = time_costs[i];
        }
    }
    // min
    time_cost_min = time_costs[0];
    for (i = 0; i < time_costs_length; i++)
    {
        if (time_costs[i] < time_cost_min){
            time_cost_min = time_costs[i];
        }
    }
    
    printf("time_costs_average: %fs\n", time_cost_avg);
    printf("time_costs_max: %fs\n", time_cost_max);
    printf("time_costs_min: %fs\n", time_cost_min);
    return 0;
}
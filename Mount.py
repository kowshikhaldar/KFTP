import psutil
import platform

#only for linux and windows

def get_mounted_drives():
    os_name=platform.system() #this will detect os 
    drive_list = []
    partition_list = psutil.disk_partitions() #get partition list
    if os_name.lower() =="windows":
        for partition in partition_list:
            drive_list.append(partition.mountpoint)
        return drive_list
    elif os_name.lower() == "linux":
         #drive_list.append("/") #uncomment this to mount root
         drive_list.append("/home/") #adding mount point manually

         for partition in partition_list:
            mount=partition.mountpoint
            #most of the relavent mount point found  in "/media/" .tested in ubuntu
            if "/media/" in mount:
                drive_list.append(mount)
         return drive_list
    else:
        print("Something Wrong with mounted drive")



if __name__=="__main__" :
    z=get_mounted_drives()
    print((z))
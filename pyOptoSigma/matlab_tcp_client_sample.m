t=tcpclient('localhost',2430)

while 1
    %write(t, int32(1)); % select stage1
    %write(t, int32(100)); % move mills of stage1
    %pause(1);
    %write(t, int32(2)); % select stage2
    %write(t, int32(-400)); % move mills of stage2
    %pause(1);
    
    write(t,unicode2native('1,200'))
    pause(1)
    
end
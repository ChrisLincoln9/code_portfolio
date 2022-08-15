function seq = pascil(N)
seq = [0,1,0];

for m = 1:N
    
    s = 0;
    
    for p = 2:length(seq)
        s(p)=seq(p) + seq(p-1);
    end
    
    seq = [s,0];
    
end

seq = seq (2:end-1);

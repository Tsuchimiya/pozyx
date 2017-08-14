filename <- c("resus-0ligne1H3mb.txt",
              "resus-0ligne2H3mb.txt",
              "resus-0ligne1V2mb.txt",
              "resus-0ligne2V2mb.txt",
              "resus-0ligne3V2mb.txt")

filenames_test2 <- c("resus-01H4m3c.txt",
               "resus-02H4m3c.txt",
               "resus-01V130cm.txt",
               "resus-02V130cm.txt",
               "resus-03V130cm.txt",
               "resus-04V130cm.txt");
filenameligneV_test2 <- c(
               "resus-02H4m3c.txt",
               "resus-02H4mleft3c.txt"
               
               );

filenames_test3 <- c(
  "resus-01H3m4bc.txt",
  "resus-02H3m4bc.txt",
  "resus-01V150cm4bc.txt",
  "resus-02V150cm4bc.txt",
  "resus-03V150cm4bc.txt",
  "resus-04V150cm4bc.txt"
  
)

filenames_test3_uwb <- c(
  "resus-01H3m4c.txt",
  "resus-02H3m4c.txt",
  "resus-01V150cm4c.txt",
  "resus-02V150cm4c.txt",
  "resus-03V150cm4c.txt"
  
)

filenames_test3_lines <- c(
  
  "resus-02H3m4bc.txt",
  "resus-02HL3m4bc.txt"
)

filenames_test3_lines <- c(

  "resus-01VL150cm4c.txt",
  "resus-01V150cm4c.txt"
)

init <- FALSE;
nb <- 0 

col <- "blue"

for (j in filenames_test3_lines){
if(nb >= 1){
  col <- "red"
}
  
df <- read.table(paste0("pozyx_ready_to_localize/",
                        j) , sep=",")
ecarts <- matrix(0,nrow=nrow(df),ncol =ncol(df))
moy_ecarts <- array(0,dim=ncol(df))
ecartype <- array(0,dim=ncol(df))
for (i in 1:ncol(df)){
  df[,i] <- as.numeric(substring(df[,i],4,9))
  moy <- mean(df[,i])
  ecarts[,i] <- abs(moy - df[,i])
  moy_ecarts[i] <- mean(ecarts[,i])
  ecartype[i] <- sqrt(mean(df[,i]^2)-mean(df[,i])^2)
}
print("-----------------------------")
print(j)
print("moy")
print(moy_ecarts)
print("ecartype")
print(ecartype)
print(paste0("lg X = ",(max(df[,2])-min(df[,2]))))
print(paste0("lg Y = ",(max(df[,1])-min(df[,1]))))
print("-----------------------------")
if(!init){
  plot(df[,2],df[,1],xlab = "X", ylab="Y", col=col,xlim = c(0,5000), ylim = c(0,8000))
  init <- TRUE
}
else{
  points(df[,2],df[,1],col=col)
}
nb <- nb + 1
min(df[,2])

}
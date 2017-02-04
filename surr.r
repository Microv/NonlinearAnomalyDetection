cdfunction <- function(time.series) {
	cd = corrDim(time.series,
             min.embedding.dim = emb.dim,
             max.embedding.dim = emb.dim + 5,
             time.lag = tau.ami, 
             min.radius = 0.001, max.radius = 50,
             n.points.radius = 40,
             do.plot=FALSE)
	plot(cd)
	cd.est = estimate(cd, regression.range=c(0.75,3),
                  use.embeddings = 5:7)
	cat("expected: 2.05  --- estimate: ",cd.est,"\n")
        return(cd.est)

}

st = surrogateTest(lor.x,significance = 0.05,one.sided = F,FUN=cdfunction, do.plot=FALSE)

plot(st, xlim = c(0,7))

mlfunction <- function(time.series) {
	sampling.period = diff(lor$time)[1]
	ml = maxLyapunov(time.series, 
                 sampling.period=sampling.period,
                 min.embedding.dim = emb.dim,
                 max.embedding.dim = emb.dim + 3,
                 time.lag = tau.ami, 
                 radius=1,
                 max.time.steps=1000,
                 do.plot=FALSE)
	plot(ml,type="l", xlim = c(0,8))
	ml.est = estimate(ml, regression.range = c(0,3),
                  do.plot = T,type="l")
	cat("expected: 0.906  --- estimate: ", ml.est,"\n")
	return(ml.est)	
	
}

st = surrogateTest(lor.x,significance = 0.05,one.sided = F,FUN=mlfunction, do.plot=FALSE)

plot(st)

sefunction <- function(time.series) {
	cd = corrDim(time.series,
             min.embedding.dim = emb.dim,
             max.embedding.dim = emb.dim + 5,
             time.lag = tau.ami, 
             min.radius = 0.001, max.radius = 50,
             n.points.radius = 40,
             do.plot=FALSE)
	se = sampleEntropy(cd, do.plot = F)
	se.est = estimate(se, do.plot = F,
                  regression.range = c(8,15))
	cat("Sample entropy estimate: ", mean(se.est), "\n")
	return(mean(se.est))	
	
}

st = surrogateTest(lor.x,significance = 0.05,one.sided = F,FUN=sefunction, do.plot=FALSE)

plot(st)









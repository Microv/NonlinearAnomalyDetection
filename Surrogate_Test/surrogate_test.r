suppressMessages(library('nonlinearTseries'))

ts = scan("timeseries.dat")

tau.ami = timeLag(ts, technique = "ami", lag.max = 100, do.plot = T)
emb.dim = estimateEmbeddingDim(ts, time.lag = tau.ami, max.embedding.dim = 22)

cdfunction <- function(time.series) {
	cd = corrDim(time.series,
             min.embedding.dim = emb.dim,
             max.embedding.dim = emb.dim + 5,
             time.lag = tau.ami, 
             min.radius = 0.001, max.radius = 50,
             n.points.radius = 40,
             do.plot=FALSE)
	plot(cd)
	cd.est = estimate(cd)
	return(cd.est)
}

st = surrogateTest(ts,significance = 0.05,one.sided = F,FUN=cdfunction, do.plot=FALSE)

#Computing statistics
#
#Null Hypothesis: Data comes from a linear stochastic process
#Reject Null hypothesis:
# 	Original data's stat is significant larger than surrogates' stats


plot(st)
dev.copy(png,'surrogate_test.png')
dev.off()

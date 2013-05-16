from main.distribution.Gaussian import Gaussian
from main.distribution.Ring import Ring
from main.mcmc.MCMCChain import MCMCChain
from main.mcmc.MCMCParams import MCMCParams
from main.mcmc.output.PlottingOutput import PlottingOutput
from main.mcmc.output.ProgressOutput import ProgressOutput
from main.mcmc.samplers.MCMCSampler import MCMCSampler
from main.tools.Visualise import Visualise
from numpy.core.function_base import linspace
from numpy.dual import cholesky
from numpy.ma.core import array, sqrt, exp, log
from numpy.matlib import eye

class AdaptiveMetropolis(MCMCSampler):
    '''
    Plain Adaptive Metropolis by Haario et al
    adapt_scale=False uses estimated covariance * "optimal scaling"
    adapt_scale=True adapts scaling to reach "optimal acceptance rate"
    '''
    def __init__(self, distribution,adapt_scale = False,\
                 mean_est=array([-2,-2]), cov_est=0.05*eye(2), \
                 learn_rate = lambda j: 1.0/sqrt(j+1.0), \
                 sample_discard=500, sample_lag=10, accstar=0.234):
        assert (len(mean_est)==distribution.dimension)
        MCMCSampler.__init__(self, distribution)
        self.globalscale = (2.38 ** 2) / distribution.dimension
        self.adapt_scale=adapt_scale
        self.learn_rate=learn_rate
        self.mean_est=mean_est
        self.cov_est=cov_est
        self.sample_discard=sample_discard
        self.sample_lag=sample_lag
        self.accstar=accstar
        self.L_R=cholesky(self.globalscale*self.cov_est)
        
    def update(self,samples,ratios):
        iter_no=len(samples)
        if iter_no > self.sample_discard and iter_no % self.sample_lag==0:
            learn_scale=self.learn_rate(float(iter_no-self.sample_discard)/self.sample_lag)
            self.cov_est = self.cov_est + learn_scale * (((self.current - self.mean_est).T).dot(self.current-self.mean_est) - self.cov_est)
            self.mean_est = self.mean_est + learn_scale* (self.current - self.mean_est)
            if self.adapt_scale:
                acc=ratios[len(ratios)-1]
                self.globalscale=exp(log(self.globalscale)+learn_scale * (exp(acc)-self.accstar))
            self.L_R=cholesky(self.globalscale*self.cov_est)
    def construct_proposal(self, y):
        return Gaussian(y, self.L_R, is_cholesky=True)
    
if __name__ == '__main__':
    distribution = Ring()
    am_sampler = AdaptiveMetropolis(distribution,adapt_scale=False)
    
    start = array([[-2, -2]])
    mcmc_params = MCMCParams(start=start, num_iterations=10000)
    chain = MCMCChain(distribution, am_sampler, mcmc_params)
    
    chain.append_mcmc_output(ProgressOutput())
    Xs = linspace(-5, 5, 50)
    Ys = linspace(-5, 5, 50)
    chain.append_mcmc_output(PlottingOutput(Xs, Ys, plot_from=3000))
    chain.run()
    
    Visualise.visualise_distribution(distribution, chain.samples)
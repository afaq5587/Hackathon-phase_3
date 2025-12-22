'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getAuthMessage, useAuth } from '@/lib/auth';
import { signIn, signUp } from '@/lib/auth-client';

export default function HomeContent() {
  const router = useRouter();
  const [message, setMessage] = useState<string | null>(null);
  const { user: session, isLoading: isSessionLoading } = useAuth();
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [signUpName, setSignUpName] = useState('');
  const [showSignUp, setShowSignUp] = useState(false);
  const [authError, setAuthError] = useState<string | null>(null);

  useEffect(() => {
    const authMessage = getAuthMessage();
    if (authMessage) {
      setMessage(authMessage);
    }
  }, []);

  if (isSessionLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-neon-dark">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-neon-cyan shadow-[0_0_15px_#00f3ff]"></div>
      </div>
    );
  }

  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-4 relative overflow-hidden bg-neon-dark circuit-bg">
      <div className="scanline" />
      
      {/* Dynamic Data Streams */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div className="data-stream" style={{ left: '10%', animationDelay: '0s' }} />
        <div className="data-stream" style={{ left: '30%', animationDelay: '2s' }} />
        <div className="data-stream" style={{ left: '60%', animationDelay: '1s' }} />
        <div className="data-stream" style={{ left: '85%', animationDelay: '3s' }} />
      </div>

      {/* Background glowing orbs */}
      <div className="absolute top-0 left-0 w-full h-full pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-neon-cyan/5 rounded-full blur-[120px] animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-neon-magenta/5 rounded-full blur-[120px] animate-pulse" style={{ animationDelay: '2s' }} />
      </div>
      
      <div className="max-w-4xl w-full grid grid-cols-1 lg:grid-cols-2 gap-8 relative z-10 transition-all duration-700">
        {/* Left Column: Hero & Branding */}
        <div className="glass-card p-10 flex flex-col justify-between neon-border h-full relative group">
          {/* Corner Ornaments */}
          <div className="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-neon-cyan/40 rounded-tl-xl pointer-events-none group-hover:border-neon-cyan transition-colors" />
          <div className="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-neon-cyan/40 rounded-br-xl pointer-events-none group-hover:border-neon-cyan transition-colors" />

          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-neon-cyan/10 border border-neon-cyan/20 mb-8">
              <div className="h-1.5 w-1.5 rounded-full bg-neon-cyan animate-pulse" />
              <span className="text-[10px] font-mono text-neon-cyan uppercase tracking-tighter">System Online // v3.2.1</span>
            </div>
            
            <h1 className="text-6xl font-bold tracking-tighter mb-4 leading-none heading-robotic glow-pulse">
              NEURAL<br />TASKER
            </h1>
            <p className="text-gray-400 text-lg mb-8 max-w-sm">
              The next generation of task management powered by advanced neural architecture.
            </p>
          </div>

          <div className="space-y-6">
            <div className="flex items-center gap-4 p-4 rounded-xl bg-white/5 border border-white/5 hover:border-neon-cyan/30 transition-all group">
              <div className="h-10 w-10 rounded-lg bg-neon-cyan/10 flex items-center justify-center text-neon-cyan">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div>
                <h4 className="text-sm font-bold text-white uppercase tracking-wider italic">Direct Interface</h4>
                <p className="text-[11px] text-gray-500 font-mono">Zero-latency command processing.</p>
              </div>
            </div>

            <div className="flex items-center gap-4 p-4 rounded-xl bg-white/5 border border-white/5 hover:border-neon-magenta/30 transition-all group">
              <div className="h-10 w-10 rounded-lg bg-neon-magenta/10 flex items-center justify-center text-neon-magenta">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <div>
                <h4 className="text-sm font-bold text-white uppercase tracking-wider italic">Secured Node</h4>
                <p className="text-[11px] text-gray-500 font-mono">Encrypted 256-bit neural link.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Interaction & Metrics */}
        <div className="flex flex-col gap-8">
          {/* Status Panel */}
          <div className="glass-card p-8 neon-border-magenta flex-1 flex flex-col justify-between relative group">
            {/* Corner Ornaments */}
            <div className="absolute top-0 left-0 w-6 h-6 border-t-2 border-l-2 border-neon-magenta/40 rounded-tl-lg pointer-events-none group-hover:border-neon-magenta transition-colors" />
            <div className="absolute bottom-0 right-0 w-6 h-6 border-b-2 border-r-2 border-neon-magenta/40 rounded-br-lg pointer-events-none group-hover:border-neon-magenta transition-colors" />

            <div>
              <div className="flex items-center justify-between mb-6">
                <h3 className="robotic-tag">Node Status</h3>
                <div className="text-[10px] text-gray-600 font-mono">ID: 0x7F4A...9E</div>
              </div>

              {session ? (
                <div className="space-y-6">
                  <div className="p-6 rounded-2xl bg-neon-cyan/5 border border-neon-cyan/20">
                    <p className="text-xs text-neon-cyan/60 font-mono uppercase mb-2">Authenticated User</p>
                    <h2 className="text-2xl font-bold text-white tracking-tight underline decoration-neon-cyan/30 underline-offset-8">
                      {session.name}
                    </h2>
                  </div>
                  <p className="text-sm text-gray-400 font-mono leading-relaxed" style={{ color: 'rgba(156, 163, 175, 1)' }}>
                    [SYSTEM] Neural link maintained. Session is active. You may return to the core interface to manage your directives.
                  </p>
                </div>
              ) : (
                <div className="space-y-6">
                  <p className="text-sm text-gray-400 font-mono leading-relaxed" style={{ color: 'rgba(156, 163, 175, 1)' }}>
                    [SYSTEM] Terminal awaits initialization. Connect your neural profile to manage global directives and tasks.
                  </p>
                  {message && (
                    <div className="bg-neon-magenta/10 border border-neon-magenta/30 text-neon-magenta px-4 py-3 rounded-lg text-xs font-mono animate-pulse">
                      [ALERT] {message}
                    </div>
                  )}
                  {authError && (
                    <div className="bg-red-500/10 border border-red-500/30 text-red-500 px-4 py-2 rounded-lg text-[10px] font-mono">
                      [AUTH_ERROR] {authError}
                    </div>
                  )}
                </div>
              )}
            </div>

            <div className="pt-8">
              {session ? (
                <div className="flex gap-3">
                  <button
                    onClick={() => router.push('/chat')}
                    className="btn btn-primary flex-1 py-5 text-base tracking-[0.2em] uppercase relative group overflow-hidden"
                  >
                    <span className="relative z-10">AI Chat</span>
                    <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-500" />
                  </button>
                  <button
                    onClick={() => router.push('/tasks')}
                    className="btn border-neon-magenta text-neon-magenta hover:bg-neon-magenta/10 flex-1 py-5 text-base tracking-[0.2em] uppercase relative group overflow-hidden"
                  >
                    <span className="relative z-10">Tasks</span>
                    <div className="absolute inset-0 bg-neon-magenta/20 translate-y-full group-hover:translate-y-0 transition-transform duration-500" />
                  </button>
                </div>
              ) : showSignUp ? (
                <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
                  <input
                    type="text"
                    placeholder="FULL NAME..."
                    value={signUpName}
                    onChange={(e) => setSignUpName(e.target.value)}
                    className="input w-full py-3 bg-white/5 border-neon-cyan/20 focus:border-neon-cyan uppercase font-mono text-xs"
                  />
                  <input
                    type="email"
                    placeholder="EMAIL ADDRESS..."
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="input w-full py-3 bg-white/5 border-neon-cyan/20 focus:border-neon-cyan uppercase font-mono text-xs"
                  />
                  <input
                    type="password"
                    placeholder="PASSWORD..."
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="input w-full py-3 bg-white/5 border-neon-cyan/20 focus:border-neon-cyan uppercase font-mono text-xs"
                  />
                  <div className="flex gap-4">
                    <button
                      onClick={() => setShowSignUp(false)}
                      className="btn border-white/10 text-white/40 hover:text-white px-6 uppercase text-xs font-mono"
                    >
                      Back
                    </button>
                    <button
                      onClick={async () => {
                        setAuthError(null);
                        const result = await signUp.email({
                          email,
                          password,
                          name: signUpName,
                          callbackURL: "/chat"
                        });

                        if (result?.error) {
                          setAuthError(result.error.message || 'Signup failed');
                        }
                      }}
                      className="btn btn-primary flex-1 py-4 uppercase tracking-[0.2em]"
                      disabled={!email || !password || !signUpName}
                    >
                      Establish Link
                    </button>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <input
                    type="email"
                    placeholder="EMAIL..."
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="input w-full py-3 bg-white/5 border-neon-cyan/20 focus:border-neon-cyan uppercase font-mono text-xs"
                  />
                  <input
                    type="password"
                    placeholder="PASSWORD..."
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="input w-full py-3 bg-white/5 border-neon-cyan/20 focus:border-neon-cyan uppercase font-mono text-xs"
                  />
                  <button
                    onClick={async () => {
                      setAuthError(null);
                      const result = await signIn.email({
                        email,
                        password,
                        callbackURL: "/chat"
                      });

                      if (result?.error) {
                        setAuthError(result.error.message || 'Invalid email or password');
                      }
                    }}
                    className="btn btn-primary w-full py-5 text-lg tracking-[0.2em] uppercase relative group overflow-hidden"
                  >
                    <span className="relative z-10 font-bold italic">Link Account // Sign In</span>
                    <div className="absolute inset-0 bg-white/10 translate-y-full group-hover:translate-y-0 transition-transform duration-500" />
                  </button>
                  
                  <button
                    onClick={() => setShowSignUp(true)}
                    className="w-full py-3 text-[10px] font-mono text-neon-cyan/60 hover:text-neon-cyan uppercase tracking-[0.3em] transition-all border border-neon-cyan/10 hover:border-neon-cyan/30 rounded-lg hover:bg-neon-cyan/5"
                  >
                    Initialize New Profile // Sign Up
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Metrics Panel */}
          <div className="glass-card p-6 border-white/5 grid grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-black/40 border border-white/5">
              <div className="text-[10px] text-gray-600 font-mono uppercase mb-1" style={{ color: 'rgba(75, 85, 99, 1)' }}>Core Load</div>
              <div className="text-xl font-bold text-white font-mono">1.2%</div>
              <div className="w-full bg-white/10 h-1 mt-2 rounded-full overflow-hidden">
                <div className="bg-neon-lime h-full w-[12%]" />
              </div>
            </div>
            <div className="p-4 rounded-xl bg-black/40 border border-white/5">
              <div className="text-[10px] text-gray-600 font-mono uppercase mb-1" style={{ color: 'rgba(75, 85, 99, 1)' }}>Latency</div>
              <div className="text-xl font-bold text-white font-mono">4ms</div>
              <div className="w-full bg-white/10 h-1 mt-2 rounded-full overflow-hidden">
                <div className="bg-neon-cyan h-full w-[4%]" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

import Link from 'next/link';

export function Sidebar() {
  return (
    <div className="w-64 h-screen bg-gray-900 text-white flex flex-col p-4 fixed left-0 top-0">
      <div className="flex items-center gap-2 mb-10 mt-2 px-2">
        <div className="w-8 h-8 rounded-lg bg-blue-500 flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/30">
          P
        </div>
        <h1 className="text-xl font-bold tracking-tight">PayTest AI</h1>
      </div>
      
      <div className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2 px-2">Menu</div>
      <nav className="flex flex-col gap-1">
        <Link href="/" className="hover:bg-gray-800 focus:bg-gray-800 px-3 py-2 rounded-lg transition-colors text-sm font-medium text-gray-300 hover:text-white flex items-center gap-3">
          Dashboard
        </Link>
        <Link href="/execute" className="hover:bg-gray-800 focus:bg-gray-800 px-3 py-2 rounded-lg transition-colors text-sm font-medium text-gray-300 hover:text-white flex items-center gap-3">
          Execute Suites
        </Link>
        <Link href="/insights" className="hover:bg-gray-800 focus:bg-gray-800 px-3 py-2 rounded-lg transition-colors text-sm font-medium text-gray-300 hover:text-white flex items-center gap-3">
          Anomaly Insights
        </Link>
      </nav>
      
      <div className="mt-auto px-2 pb-4">
        <div className="bg-gray-800/50 p-4 rounded-xl border border-gray-700/50">
          <p className="text-xs text-gray-400 mb-2">Simulating Next-Gen Payments</p>
          <div className="w-full bg-gray-700 rounded-full h-1.5">
            <div className="bg-blue-500 h-1.5 rounded-full w-3/4"></div>
          </div>
        </div>
      </div>
    </div>
  );
}

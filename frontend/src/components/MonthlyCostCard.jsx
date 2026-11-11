function MonthlyCostCard({comparison}) {
if (comparison.status !== "ok") {
    return (
        <div className="mt-8 rounded-2xl bg-white p-6 text-left shadow-sm">
            <p className="text-sm text-slate-600">
                {comparison.summary}
            </p>
        </div>
    )
}
    const badgeColor = comparison.difference < 0 ? "bg-emerald-50 text-emerald-700" : "bg-rose-50 text-rose-700"
    return (
        <div className="mt-8 rounded-2xl bg-white p-6 text-left shadow-sm">
            <h2 className="text-sm font-medium uppercase tracking-widest text-slate-500">
                Monthly Cost
            </h2>

              <div className="mt-4 grid grid-cols-2 gap-4">
                  <div>
                      <p className="text-sm text-slate-600">
                          Current Policy
                      </p>
                      <p className="mt-2 text-3xl font-semibold tracking-tight text-slate-900">
                         ${comparison.current_cost.toFixed(2)}
                      </p>
                  </div>
                  <div>
                      <p className="text-sm text-slate-600">
                          New Quote
                      </p>
                      <p className="mt-2 text-3xl font-semibold tracking-tight text-slate-900">
                         ${comparison.new_cost.toFixed(2)}
                      </p>

                  </div>
              </div>
          <p className={`mt-4 inline-block rounded-full px-3 py-1 text-sm font-medium ${badgeColor}`}>
        {comparison.summary}
      </p>
    </div>
  )
}

export default MonthlyCostCard



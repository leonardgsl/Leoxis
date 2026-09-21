const B=[{m:18,l:'Strong'},{m:24,l:'Healthy'},{m:36,l:'Requires justification'},{m:Infinity,l:'High capital-return concern'}];
const n=v=>Number.isFinite(Number(v))?Number(v):0;
function calc(i,a={salesPct:0,gmPoints:0,opexPct:0}){
 const sales=n(i.projectedMonthlySales)*(1+n(a.salesPct)/100),gm=n(i.grossMarginPct)+n(a.gmPoints),tr=sales*n(i.turnoverRentPct)/100;
 const raw=i.opexMode==='total'?n(i.totalMonthlyStoreOpex):n(i.payroll)+n(i.utilities)+n(i.maintenance)+n(i.otherStoreOpex);
 const op=raw*(1+n(a.opexPct)/100),fixed=n(i.monthlyRent)+n(i.serviceCharge)+op,gp=sales*gm/100,ebitda=gp-fixed-tr;
 const margin=sales?ebitda/sales*100:0,investment=n(i.capex)+n(i.deposit),payback=ebitda>0?investment/ebitda:null;
 const occupancy=sales?(n(i.monthlyRent)+n(i.serviceCharge)+tr)/sales*100:0,contribution=gm-n(i.turnoverRentPct),breakeven=contribution>0?fixed/(contribution/100):null;
 return {sales,gm,ebitda,margin,investment,payback,occupancy,contribution,fixed,breakeven};
}
const tMargin=(b,t)=>b.contribution<=t?null:b.fixed/((b.contribution-t)/100);
const tPay=(b,t)=>t<=0||b.contribution<=0?null:(b.fixed+b.investment/t)/(b.contribution/100);
function evidence(i){const e=i.evidence||{},c=[e.sales,e.rent,e.capex,e.margin,e.footfall||!!n(i.footfall),e.catchment||!!n(i.catchmentPopulation),!!i.competitors,!!n(i.leaseTermYears),!!n(i.rampUpMonths)],coverage=Math.round(c.filter(Boolean).length/c.length*100);return{coverage,level:coverage>=80?'Strong':coverage>=60?'Moderate':'Weak'}}
export default function handler(req,res){
 if(req.method!=='POST')return res.status(405).json({ok:false,error:'Method not allowed'});
 try{
  const i=req.body?.input||{},tm=n(req.body?.targetMargin)||10,tp=n(req.body?.targetPayback)||24,base=calc(i);
  const downside=calc(i,{salesPct:-10,gmPoints:-n(i.grossMarginPct)*.10,opexPct:10}),upside=calc(i,{salesPct:10,gmPoints:n(i.grossMarginPct)*.05});
  const ev=evidence(i),ms=tMargin(base,tm),ps=tPay(base,tp),required=Math.max(ms||0,ps||0),gap=base.sales&&required?(required/base.sales-1)*100:null;
  const baseStatus=(base.ebitda<=0||base.payback===null)?'RED':(base.margin>=tm&&base.payback<=tp?'GREEN':'AMBER');
  const downsideRisk=downside.ebitda<=0?'RED':'AMBER';
  const status=(baseStatus==='RED'||ev.coverage<60)?'RED':(baseStatus==='GREEN'&&downsideRisk!=='RED'&&ev.coverage>=80?'GREEN':'AMBER');
  let action,reason;
  if(status==='GREEN'){action='PROCEED TO NEXT DECISION STAGE';reason='Core economics meet the selected working targets and evidence coverage is strong. Validate final downside assumptions before commitment.'}
  else if(status==='RED'){action='DO NOT COMMIT YET';reason='Base economics or critical evidence materially fail the current decision thresholds. Rework the case before commitment.'}
  else if(ev.coverage<60){action='HOLD / GATHER EVIDENCE';reason='The result is dominated by evidence gaps. Validate the key assumptions before relying on the economics.'}
  else{action='PROCEED TO DD / REWORK TERMS';reason='Base economics are close to target, but downside resilience is weak. Validate the binding assumptions and improve controllable economics before commitment.'}
  const interp=base.payback===null?'No payback':B.find(x=>base.payback<=x.m).l;
  return res.status(200).json({ok:true,engine:'LEOXIS_EXPANSION_VNEXT_STAGE11',status,baseStatus,downsideRisk,base,downside,upside,evidence:ev,targets:{targetMargin:tm,targetPayback:tp,marginSales:ms,paybackSales:ps,requiredSales:required,salesGapPct:gap},benchmark:{payback:{type:'LEOXIS working reference',interpretation:interp,bands:['≤18m Strong','18–24m Healthy','24–36m Requires justification','>36m High concern']}},recommendation:{action,reason},disclaimer:'Working references are decision-support heuristics, not universal retail industry standards.'});
 }catch(e){return res.status(400).json({ok:false,error:'Unable to analyse case'})}
}

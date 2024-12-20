-- Penlight 1.11.0-1 | /lua/pl/pretty.lua | https://github.com/lunarmodules/Penlight | License: MIT | Minified using https://www.npmjs.com/package/luamin/v/1.0.4
-- Copyright (C) 2009-2016 Steve Donovan, David Manura.
-- Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
-- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
-- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
local a=table.insert;local b=table.concat;local c,d=math.floor,math.huge;local e=math.type;local f=require'pl.utils'local g=require'pl.lexer'local h=require'debug'local i=require'pl.stringx'.quote_string;local j=f.assert_arg;local k=tostring;local function tostring(l)if type(l)~="number"then return k(l)elseif l~=l then return"NaN"elseif l==d then return"Inf"elseif l==-d then return"-Inf"elseif(_VERSION~="Lua 5.3"or e(l)=="integer")and c(l)==l then return("%d"):format(l)else local m=("%.14g"):format(l)if _VERSION=="Lua 5.3"and e(l)=="float"and not m:find("%.")then m=m:gsub("%d+","%0.0",1)end;return m end end;local n={}local function o()local p={}p.hook,p.mask,p.count=h.gethook()if p.hook~="external hook"then h.sethook()end;p.string_mt=getmetatable("")h.setmetatable("",nil)return p end;local function q(p)if p then h.setmetatable("",p.string_mt)if p.hook~="external hook"then h.sethook(p.hook,p.mask,p.count)end end end;function n.read(r)j(1,r,'string')if r:find'^%s*%-%-'then r=r:gsub('%-%-.-\n','')end;if not r:find'^%s*{'then return nil,"not a Lua table"end;if r:find'[^\'"%w_]function[^\'"%w_]'then local s=g.lua(r)for t,u in s do if t=='keyword'and u=='function'then return nil,"cannot have functions in table definition"end end end;r='return '..r;local v,w=f.load(r,'tbl','t',{})if not v then return nil,w end;local x=o()local y,z=pcall(v)q(x)if y then return z else return nil,z end end;function n.load(r,p,A)p=p or{}if A then local s=g.lua(r)for t,u in s do if t=='keyword'and(u=='for'or u=='repeat'or u=='function'or u=='goto')then return nil,"looping not allowed"end end end;local v,w=f.load(r,'tbl','t',p)if not v then return nil,w end;local x=A and o()local y,w=pcall(v)q(x)if not y then return nil,w end;return p end;local function B(u)if not u then return''else if u:find' 'then u=i(u)end end;return u end;local C;local function D(r)return type(r)=='string'and r:find('^[%a_][%w_]*$')and not C[r]end;local function E(r)if type(r)=='table'then return n.write(r,'')else return i(r)end end;local function F(G,H)if not G then H=E(H)H=H:find("^%[")and" "..H.." "or H end;return'['..H..']'end;function n.write(I,J,K)if type(I)~='table'then local m=tostring(I)if type(I)=='string'then return E(I)end;return m,'not a table'end;if not C then C=g.get_keywords()end;local L=' = 'if J==''then L='='end;J=J or'  'local M={}local N=''local O={}local function P(r)if#r>0 then N=N..r end end;local function Q(r)if#N>0 then N=N..r;a(M,N)N=''else a(M,r)end end;local function R()local S=#M;local T=M[S]:sub(-1,-1)if T==','then M[S]=M[S]:sub(1,-2)end end;local U=function(t)local V=0;local y,u;local W=function()return t[V]end;return function()V=V+1;y,u=pcall(W)if u==nil or not y then return end;return V,t[V]end end;local X=function(t)local Y,u,y;local W=function()return next(t,Y)end;return function()y,Y,u=pcall(W)if not y then return end;return Y,u end end;local Z;Z=function(t,_,a0)local a1=type(t)if a1~='string'and a1~='table'then Q(B(tostring(t))..',')elseif a1=='string'then Q(i(t)..",")elseif a1=='table'then if O[t]then Q('<cycle>,')return end;O[t]=true;local a2=a0 ..J;Q('{')local a3={}if not K then for V,a4 in U(t)do P(a0)Z(a4,a0,a2)a3[V]=true end end;local a5={}for Y,u in X(t)do if type(Y)~='number'then a5[#a5+1]=Y end end;table.sort(a5,function(a6,a7)if type(a6)==type(a7)and type(a6)=='string'then return a6<a7 end;return type(a6)=='boolean'or type(a7)~='boolean'and type(a6)=='table'end)local function a8(H,a4)local a9=type(H)local G=a9=='number'if K then H=tostring(H)P(a0 ..F(G,H)..L)Z(a4,a0,a2)else if not G or not a3[H]then if a9~='string'then H=tostring(H)end;if G or not D(H)then H=F(G,H)end;P(a0 ..H..L)Z(a4,a0,a2)end end end;for V=1,#a5 do local H=a5[V]local a4=t[H]a8(H,a4)end;for H,a4 in X(t)do if type(H)=='number'then a8(H,a4)end end;O[t]=nil;R()Q(_..'},')else Q(tostring(t)..',')end end;Z(I,'',J)R()return b(M,#J>0 and'\n'or'')end;function n.dump(t,aa)if not aa then print(n.write(t))return true else return f.writefile(aa,n.write(t))end end;function n.debug(...)local S=select("#",...)local t={...}for V=1,S do local l=t[V]if l==nil then l="<nil>"end;t[V]=nil;t["arg "..V]=l end;print(n.write(t))return true end;local ab,ac={'B','KiB','MiB','GiB'},{'','K','M','B'}local function ad(a4)local ae=math.floor(a4/1000)if ae>0 then return ad(ae)..','..tostring(a4%1000)else return tostring(a4)end end;function n.number(af,ag,ah)local ai='%.'..(ah or 1)..'f%s'if ag=='T'then return ad(af)else local aj,ak;if ag=='M'then ak=1024;aj=ab else ak=1000;aj=ac end;local al=ak;local Y=1;while af>=al and Y<=#aj do al=al*ak;Y=Y+1 end;al=al/ak;if Y>#aj then Y=Y-1;al=al/ak end;if Y>1 then return ai:format(af/al,aj[Y]or'duh')else return af..aj[1]end end end;return setmetatable(n,{__call=function(self,...)return self.debug(...)end})

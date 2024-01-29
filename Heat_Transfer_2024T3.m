%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Jose G Barrera
% 20240125
% This code uses the ODE Toolkit and provided website example to simulate 
% the heat transfer of a 2024-T3 AL (1m x 0.5m x 0.01m).
% Only meant as an approximation. 
% Please have PDE Toolbox Installed.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Constants and Parameters
k = 121; % Thermal conductivity of 2024-T3, W/(m-K)
rho = 2780; % Density of 2024-T3, kg/m^3
specificHeat = 875; % Specific heat of copper, J/(kg-K)
thick = 0.01; % Plate thickness in meters
stefanBoltz = 5.670373e-8; % Stefan-Boltzmann constant, W/(m^2-K^4)
hCoeff = 1; % Convection coefficient, W/(m^2-K)
ta = 300; % Ambient temperature, degrees-Kelvin
emiss = 0.5; % Emissivity of the plate surface
width = 1; % Plate width in meters
height = 0.5; % Plate height in meters
hmax = 0.1; % Maximum element size for mesh

% Geometry Definition
gdm = [3, 4, 0, width, width, 0, 0, 0, height, height]';
g = decsg(gdm, 'S1', ('S1')');

% PDE Model Creation
model = createpde;

% Apply Geometry to the Model
geometryFromEdges(model, g);

% PDE Coefficients
c = thick * k;
f = 2 * hCoeff * ta + 2 * emiss * stefanBoltz * ta^4;
d = thick * rho * specificHeat;
a = @(~, state) 2 * hCoeff + 2 * emiss * stefanBoltz * state.u.^3;

% Specify Coefficients and Boundary Conditions
specifyCoefficients(model, 'm', 0, 'd', 0, 'c', c, 'a', a, 'f', f);
applyBoundaryCondition(model, 'dirichlet', 'Edge', 4, 'u', 1000);

% Mesh Generation
msh = generateMesh(model, 'Hmax', hmax);

% Solve PDE
R = solvepde(model);
u = R.NodalSolution;

% Plot Solution
figure; 
pdeplot(model, 'XYData', u, 'Contour', 'on', 'ColorMap', 'jet');
title('Temperature in the Plate, Steady State Solution');
xlabel('X-coordinate, meters');
ylabel('Y-coordinate, meters');
axis([-.1, 1.1, -.1, 0.6]);

% Extract Node Positions
p = msh.Nodes;

% Display Temperature at the Top Edge of the Plate
fprintf('Temperature at the top edge of the plate = %5.1f degrees-K\n', u(2));

specifyCoefficients(model,"m",0,"d",d,"c",c,"a",a,"f",f);
endTime = 5000;
tlist = 0:50:endTime;

setInitialConditions(model,300);

setInitialConditions(model,1000,"Edge",4);

model.SolverOptions.RelativeTolerance = 1.0e-3; 
model.SolverOptions.AbsoluteTolerance = 1.0e-4;

R = solvepde(model,tlist);
u = R.NodalSolution;
figure; 
plot(tlist,u(2,:)); 
grid on
title(["Temperature Along the Right Edge of " ...
       "the Plate as a Function of Time"])
xlabel("Time, seconds")
ylabel("Temperature, degrees-Kelvin")

figure;
pdeplot(model,"XYData",u(:,end),"Contour","on","ColorMap","jet");
title(sprintf(['Temperature In The Plate,' ...
               'Transient Solution( %d seconds)\n'],tlist(1,end)));
xlabel("X-coordinate, meters")
ylabel("Y-coordinate, meters")
axis equal;
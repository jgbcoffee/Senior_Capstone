%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Jose G Barrera
% 20240125
% This code uses the ODE Toolkit to simulate 
% the applied load on a cantelevered 2024-T3 AL (1m x 0.5m x 0.01m).
% Only meant as an approximation. Next time, I'll just upload a CAD file
% that should be more straightforward.
% Please have PDE Toolbox Installed.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Defining Metal dimensions
length = 1.0; % In meters
width = 0.5; % In meters
thickness = 0.01; % In meters

% PDE model creation
pdem = createpde('structural','static-solid');

% Geoetry Definition
modelLength = [0, length, length, 0, 0, length, length, 0];
modelWidth = [0, 0, width, width, 0, 0, width, width];
modelHeight = [0, 0, 0, 0, thickness, thickness, thickness, thickness];
model = [modelLength; modelWidth; modelHeight];

% Triangulating
DT = delaunayTriangulation(model');

% Converting triangulation to a geometry
[gm, ~] = geometryFromMesh(pdem, DT.Points', DT.ConnectivityList');

% Generate mesh with specified maximum element size
generateMesh(pdem, 'Hmax', 0.05); % Adjust 'Hmax' for mesh size

% Defining structural properties
structuralProperties(pdem,'YoungsModulus',73.4e9,'PoissonsRatio',0.33);

% Applying boundary conditions
structuralBC(pdem,'Face',2,'Constraint','fixed');

% Applying distributed load on the opposite face
distributedLoad = 1000; % Newtons per meter
structuralBoundaryLoad(pdem,'Face',5,'SurfaceTraction',[0; 0; -distributedLoad]);

% Solve PDE
result = solve(pdem);

% Plotting Von Mises Stress Distribution
pdeplot3D(pdem, 'ColorMapData', result.VonMisesStress)
% pdegplot(pdem,"FaceLabels","on","FaceAlpha",0.5)
title('Von Mises Stress Distribution')



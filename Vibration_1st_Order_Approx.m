%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Jose G Barrera
% 20240125
% The purpose of this code is to complete a 1st order approximation of
% metal vibrations due to an external force. The approximation is modeled
% After a Spring-mass-damped system (Metal) and external force (rocket)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Defining system constants, Note: Damping coefficients taken from 
% Vince Adams and Abraham Askenazi
% Building Better Products with Finite Element Analysis
m = 10; % Mass of Metal (kg)
k = 16; % Spring constant of Aluminum (N/m) derived through young's modulus
c = 0.04; % Damping coefficient (N*s/m) "Continous Metal Structure"

% Natural frequency and damping ratio
wn = sqrt(k / m); % Natural frequency (rad/s)
zeta = c / (2*sqrt(m*k)); % Damping ratio

% Defining external forces from rocket
F0 = 100; % Amplitude of force (N) 
f = 30; % Frequency of force (Hz)
omega = 2*pi*f; % Angular frequency (rad/s)

% Time vector
t = 0:0.01:5; % Time from 0 to 5 seconds with 0.01 second intervals


% Spring mass damped system with external force ODE
odefun = @(t, y) [y(2); (F0*cos(omega*t) - c*y(2) - k*y(1)) / m];
y0 = [0; 0]; % Initial conditions (initial displacement and velocity)

% ODE Solver
[t, y] = ode45(odefun, t, y0);

% Plot
figure;
plot(t, y(:,1));
grid on;
xlabel('Time (s)');
ylabel('Displacement (m)');
title('Vibrational Response of Metal Piece due to Rocket Engine');

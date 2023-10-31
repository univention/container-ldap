# ldap-server

![Version: 0.0.1](https://img.shields.io/badge/Version-0.0.1-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square)

A Helm Chart that deploys a standalone OpenLDAP server

**Homepage:** <https://zendis.de>

## Source Code

* <https://git.knut.univention.de/univention/customers/dataport/upx/container-ldap/-/tree/main/helm/ldap-server?ref_type=heads>

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| oci://registry.souvap-univention.de/souvap/tooling/charts/bitnami-charts | common | ^2.x.x |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| additionalAnnotations | object | `{}` | Additional custom annotations to add to all deployed objects. |
| additionalLabels | object | `{}` | Additional custom labels to add to all deployed objects. |
| affinity | object | `{}` | Affinity for pod assignment. Ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity Note: podAffinityPreset, podAntiAffinityPreset, and nodeAffinityPreset will be ignored when it's set. |
| containerSecurityContext.allowPrivilegeEscalation | bool | `false` | Enable container privileged escalation. |
| containerSecurityContext.capabilities | object | `{"drop":["ALL"]}` | Security capabilities for container. |
| containerSecurityContext.enabled | bool | `true` | Enable security context. |
| containerSecurityContext.readOnlyRootFilesystem | bool | `true` | Mounts the container's root filesystem as read-only. |
| containerSecurityContext.runAsGroup | int | `101` | Process group id. |
| containerSecurityContext.runAsNonRoot | bool | `true` | Run container as a user. |
| containerSecurityContext.runAsUser | int | `101` | Process user id. |
| containerSecurityContext.seccompProfile.type | string | `"RuntimeDefault"` | Disallow custom Seccomp profile by setting it to RuntimeDefault. |
| extraEnvVars | list | `[]` | Array with extra environment variables to add to containers.  extraEnvVars:   - name: FOO     value: "bar" |
| extraSecrets | list | `[]` | Optionally specify a secret to create (primarily intended to be used in development environments to provide custom certificates) |
| extraVolumeMounts | list | `[]` | Optionally specify an extra list of additional volumeMounts. |
| extraVolumes | list | `[]` | Optionally specify an extra list of additional volumes. |
| fullnameOverride | string | `""` | Provide a name to substitute for the full names of resources. |
| global.imagePullPolicy | string | `"IfNotPresent"` | Define an ImagePullPolicy.  Ref.: https://kubernetes.io/docs/concepts/containers/images/#image-pull-policy  "IfNotPresent" => The image is pulled only if it is not already present locally. "Always" => Every time the kubelet launches a container, the kubelet queries the container image registry to             resolve the name to an image digest. If the kubelet has a container image with that exact digest cached             locally, the kubelet uses its cached image; otherwise, the kubelet pulls the image with the resolved             digest, and uses that image to launch the container. "Never" => The kubelet does not try fetching the image. If the image is somehow already present locally, the            kubelet attempts to start the container; otherwise, startup fails. |
| global.imagePullSecrets | list | `[]` | Credentials to fetch images from private registry. Ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/  imagePullSecrets:   - "docker-registry" |
| global.imageRegistry | string | `"docker.io"` | Container registry address. |
| imagePullPolicy | string | `"IfNotPresent"` | Image pull policy. This setting has higher precedence than global.imagePullPolicy. |
| imagePullSecrets | list | `[]` | Credentials to fetch images from private registry. Ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/  imagePullSecrets:   - "docker-registry" |
| images.dhInitContainer.imagePullPolicy | string | `"IfNotPresent"` |  |
| images.dhInitContainer.registry | string | `"docker.io"` |  |
| images.dhInitContainer.repository | string | `"alpine/openssl"` |  |
| images.dhInitContainer.tag | string | `"3.1.3@sha256:caa8dde43c9b0a98a3703c74dfb0bb3e8fb6a75a4a873a0c76fbb7e015d00bc2"` |  |
| images.ldapServer.imagePullPolicy | string | `"IfNotPresent"` | Image pull policy. This setting has higher precedence than global.imagePullPolicy. |
| images.ldapServer.imagePullSecrets | list | `[]` |  |
| images.ldapServer.repository | string | `"souvap/tooling/images/univention-ldap/ldap-server"` | Container registry address. This setting has higher precedence than global.registry. registry: "" |
| images.ldapServer.tag | string | `"latest"` |  |
| ingress.annotations | object | `{}` | Define custom ingress annotations. annotations:   nginx.ingress.kubernetes.io/rewrite-target: / |
| ingress.enabled | bool | `false` | Enable creation of Ingress. |
| ingress.host | string | `""` | Define the Fully Qualified Domain Name (FQDN) where application should be reachable. |
| ingress.ingressClassName | string | `"nginx"` | The Ingress controller class name. |
| ingress.path | string | `"/"` | Define the Ingress path. |
| ingress.pathType | string | `"Prefix"` | Each path in an Ingress is required to have a corresponding path type. Paths that do not include an explicit pathType will fail validation. There are three supported path types:  "ImplementationSpecific" => With this path type, matching is up to the IngressClass. Implementations can treat this                             as a separate pathType or treat it identically to Prefix or Exact path types. "Exact" => Matches the URL path exactly and with case sensitivity. "Prefix" => Matches based on a URL path prefix split by /.  Ref.: https://kubernetes.io/docs/concepts/services-networking/ingress/#path-types |
| ingress.tls | object | `{"enabled":true,"secretName":""}` | Secure an Ingress by specifying a Secret that contains a TLS private key and certificate.  Ref.: https://kubernetes.io/docs/concepts/services-networking/ingress/#tls |
| ingress.tls.enabled | bool | `true` | Enable TLS/SSL/HTTPS for Ingress. |
| ingress.tls.secretName | string | `""` | The name of the kubernetes secret which contains a TLS private key and certificate. Hint: This secret is not created by this chart and must be provided. |
| ldapServer.config.domainname | string | `"univention-organization.intranet"` | Internal domain name of the UCS machine |
| ldapServer.config.environment | string | `"production"` | TODO: Clarify usage of this parameter |
| ldapServer.config.ldapBaseDn | string | `"dc=univention-organization,dc=intranet"` | Base DN of the LDAP directory |
| ldapServer.config.logLevel | string | `"stats"` | Log level for slapd.    Pass a comma-separated list of values from the <a href="https://openldap.org/doc/admin24/runningslapd.html#Command-Line%20Options">OpenLDAP docs</a>.    Example: `"conn,stats"`. |
| ldapServer.config.samlMetadataUrl | string | `""` | URL of the IdP that contains the SAML metadata. samlMetadataUrl: "http://myportal.local:8097/realms/ucs/protocol/saml/descriptor" |
| ldapServer.config.samlMetadataUrlInternal | string | `""` | Internal URL of the IdP to download SAML metadata from,    in the case that `saml_metadata_url` is not visible to the container. samlMetadataUrlInternal: "http://keycloak.myportal.local/realms/ucs/protocol/saml/descriptor" |
| ldapServer.config.samlServiceProviders | string | `""` | A comma separated list of SAML2 Service Provider URLs (must be defined) samlServiceProviders: "http://myportal.local:8000/univention/saml/metadata,http://myportal.local:8000/auth/realms/ucs" |
| ldapServer.credentialSecret | object | `{}` | Optional reference to a different secret for credentials credentialSecret:  name: "custom-credentials"  adminPasswordKey: "adminPassword" |
| ldapServer.generateDHparam | bool | `true` |  |
| ldapServer.legacy.sharedRunSize | string | `"1Gi"` |  |
| ldapServer.tls.caCertificateFile | string | `"/certificates/ca.crt"` |  |
| ldapServer.tls.certificateFile | string | `"/certificates/tls.crt"` |  |
| ldapServer.tls.certificateKeyFile | string | `"/certificates/tls.key"` |  |
| ldapServer.tls.certificateSecret | object | `{}` | Optional reference to the secret to use for reading certificates certificateSecret:  name: "custom-tls" |
| ldapServer.tls.dhparamSecret | object | `{}` | Optional reference to the secret to use for reading Diffie-Hellman parameters dhparamSecret:  name: "custom-dhparam" |
| ldapServer.tls.enabled | bool | `true` |  |
| lifecycleHooks | object | `{}` | Lifecycle to automate configuration before or after startup. |
| livenessProbe.enabled | bool | `true` | Enables kubernetes LivenessProbe. |
| livenessProbe.failureThreshold | int | `10` | Number of failed executions until container is terminated. |
| livenessProbe.initialDelaySeconds | int | `15` | Delay after container start until LivenessProbe is executed. |
| livenessProbe.periodSeconds | int | `20` | Time between probe executions. |
| livenessProbe.successThreshold | int | `1` | Number of successful executions after failed ones until container is marked healthy. |
| livenessProbe.timeoutSeconds | int | `5` | Timeout for command return. |
| nameOverride | string | `""` | String to partially override release name. |
| nodeSelector | object | `{}` | Node labels for pod assignment. Ref: https://kubernetes.io/docs/user-guide/node-selection/ |
| persistence.accessModes | list | `["ReadWriteOnce"]` | The volume access modes, some of "ReadWriteOnce", "ReadOnlyMany", "ReadWriteMany", "ReadWriteOncePod".  "ReadWriteOnce" => The volume can be mounted as read-write by a single node. ReadWriteOnce access mode still can                    allow multiple pods to access the volume when the pods are running on the same node. "ReadOnlyMany" => The volume can be mounted as read-only by many nodes. "ReadWriteMany" => The volume can be mounted as read-write by many nodes. "ReadWriteOncePod" => The volume can be mounted as read-write by a single Pod. Use ReadWriteOncePod access mode if                       you want to ensure that only one pod across whole cluster can read that PVC or write to it.  |
| persistence.annotations | object | `{}` | Annotations for the PVC. |
| persistence.dataSource | object | `{}` | Custom PVC data source. |
| persistence.enabled | bool | `true` | Enable data persistence (true) or use temporary storage (false). |
| persistence.existingClaim | string | `""` | Use an already existing claim. |
| persistence.labels | object | `{}` | Labels for the PVC. |
| persistence.selector | object | `{}` | Selector to match an existing Persistent Volume (this value is evaluated as a template).  selector:   matchLabels:     app: my-app  |
| persistence.size | string | `"10Gi"` | The volume size with unit. |
| persistence.storageClass | string | `""` | The (storage) class of PV. |
| podAnnotations | object | `{}` | Pod Annotations. Ref: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ |
| podLabels | object | `{}` | Pod Labels. Ref: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ |
| podSecurityContext.enabled | bool | `true` | Enable security context. |
| podSecurityContext.fsGroup | int | `101` | If specified, all processes of the container are also part of the supplementary group. |
| podSecurityContext.fsGroupChangePolicy | string | `"Always"` | Change ownership and permission of the volume before being exposed inside a Pod. |
| prometheus.prometheusRule.enabled | bool | `false` | Enable Prometheus PrometheusRule. This requires "monitoring.coreos.com" CRD. |
| prometheus.prometheusRule.groups | list | `[]` | Groups, containing the alert rules. |
| prometheus.prometheusRule.labels | object | `{}` | Additional labels for PrometheusRule resource. |
| prometheus.prometheusRule.namespace | string | `""` | Namespace where to deploy serviceMonitor resource to. |
| prometheus.serviceMonitor.enabled | bool | `false` | Enable Prometheus ServiceMonitor. This requires "monitoring.coreos.com" CRD. |
| prometheus.serviceMonitor.honorLabels | bool | `false` | honorLabels chooses the metrics labels on collisions with target labels. |
| prometheus.serviceMonitor.interval | string | `"30s"` | Interval at which metrics should be scraped. |
| prometheus.serviceMonitor.jobLabel | string | `""` | The name of the label on the target service to use as the job name in prometheus. |
| prometheus.serviceMonitor.labels | object | `{}` | Additional labels for ServiceMonitor resource. |
| prometheus.serviceMonitor.metricRelabelings | list | `[]` | MetricRelabelConfigs to apply to samples before ingestion. |
| prometheus.serviceMonitor.namespace | string | `""` | Namespace where to deploy serviceMonitor resource to. |
| prometheus.serviceMonitor.path | string | `"/metrics"` | Metrics service HTTP path. |
| prometheus.serviceMonitor.relabelings | list | `[]` | RelabelConfigs to apply to samples before scraping. |
| prometheus.serviceMonitor.scrapeTimeout | string | `"30s"` | Specify the timeout after which the scrape is ended. |
| readinessProbe.enabled | bool | `true` | Enables kubernetes ReadinessProbe. |
| readinessProbe.failureThreshold | int | `10` | Number of failed executions until container is terminated. |
| readinessProbe.initialDelaySeconds | int | `15` | Delay after container start until ReadinessProbe is executed. |
| readinessProbe.periodSeconds | int | `20` | Time between probe executions. |
| readinessProbe.successThreshold | int | `1` | Number of successful executions after failed ones until container is marked healthy. |
| readinessProbe.timeoutSeconds | int | `5` | Timeout for command return. |
| replicaCount | int | `1` | Set the amount of replicas of deployment. |
| resources.limits.cpu | int | `1` | The max number of CPUs to consume. |
| resources.limits.memory | string | `"1Gi"` | The max number of RAM to consume. |
| resources.requests.cpu | string | `"100m"` | The number of CPUs which has to be available on the scheduled node. |
| resources.requests.memory | string | `"512Mi"` | The number of RAM which has to be available on the scheduled node. |
| service.annotations | object | `{}` | Additional custom annotations. |
| service.enabled | bool | `true` | Enable kubernetes service creation. |
| service.ports.ldap.containerPort | int | `389` | Internal port. |
| service.ports.ldap.port | int | `389` | Accessible port. |
| service.ports.ldap.protocol | string | `"TCP"` | service protocol. |
| service.ports.ldaps.containerPort | int | `636` | Internal port. |
| service.ports.ldaps.port | int | `636` | Accessible port. |
| service.ports.ldaps.protocol | string | `"TCP"` | service protocol. |
| service.type | string | `"ClusterIP"` | Choose the kind of Service, one of "ClusterIP", "NodePort" or "LoadBalancer". |
| serviceAccount.annotations | object | `{}` | Additional custom annotations for the ServiceAccount. |
| serviceAccount.automountServiceAccountToken | bool | `false` | Allows auto mount of ServiceAccountToken on the serviceAccount created. Can be set to false if pods using this serviceAccount do not need to use K8s API. |
| serviceAccount.create | bool | `true` | Enable creation of ServiceAccount for pod. |
| serviceAccount.labels | object | `{}` | Additional custom labels for the ServiceAccount. |
| startupProbe.enabled | bool | `true` | Enables kubernetes StartupProbe. |
| startupProbe.failureThreshold | int | `10` | Number of failed executions until container is terminated. |
| startupProbe.initialDelaySeconds | int | `15` | Delay after container start until StartupProbe is executed. |
| startupProbe.periodSeconds | int | `20` | Time between probe executions. |
| startupProbe.successThreshold | int | `1` | Number of successful executions after failed ones until container is marked healthy. |
| startupProbe.timeoutSeconds | int | `5` | Timeout for command return. |
| terminationGracePeriodSeconds | string | `""` | In seconds, time the given to the pod needs to terminate gracefully. Ref: https://kubernetes.io/docs/concepts/workloads/pods/pod/#termination-of-pods |
| tolerations | list | `[]` | Tolerations for pod assignment. Ref: https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/ |
| topologySpreadConstraints | list | `[]` | Topology spread constraints rely on node labels to identify the topology domain(s) that each Node is in. Ref: https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints/  topologySpreadConstraints:   - maxSkew: 1     topologyKey: failure-domain.beta.kubernetes.io/zone     whenUnsatisfiable: DoNotSchedule |
| updateStrategy.type | string | `"RollingUpdate"` | Set to Recreate if you use persistent volume that cannot be mounted by more than one pods to make sure the pods are destroyed first. |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.11.0](https://github.com/norwoodj/helm-docs/releases/v1.11.0)

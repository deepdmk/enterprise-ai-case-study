/**
 * Get the correct asset path accounting for basePath in production
 */
export function getAssetPath(path: string): string {
  const basePath = process.env.NODE_ENV === 'production'
    ? '/enterprise-ai-case-study'
    : '';

  // Ensure path starts with /
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;

  return `${basePath}${normalizedPath}`;
}
